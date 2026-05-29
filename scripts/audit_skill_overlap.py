#!/usr/bin/env python3
"""Audit local skill overlap before creating or changing a skill."""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


STOPWORDS = {
    "about", "across", "agent", "agents", "also", "and", "any", "are", "asks",
    "based", "before", "between", "codex", "create", "creating", "edit",
    "existing", "file", "files", "for", "from", "help", "into", "local",
    "manage", "modify", "needs", "other", "read", "related", "should", "skill",
    "skills", "that", "the", "their", "them", "this", "through", "update",
    "user", "users", "using", "when", "with", "work", "wants", "需要", "使用",
}

HIGH_VALUE_TERMS = {
    "article", "blog", "content", "copywriting", "debug", "design", "doc",
    "docx", "feishu", "frontend", "lark", "pdf", "polish", "ppt", "pptx",
    "presentation", "review", "seo", "slides", "test", "ui", "ux", "write",
    "writing", "chinese", "style", "tutorial", "文档", "写作", "文章", "润色", "飞书",
}


@dataclass
class Skill:
    root: Path
    directory: str
    name: str
    description: str
    path: Path


def extract_frontmatter(text: str) -> dict[str, str]:
    if text.startswith("\ufeff"):
        text = text[1:]
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not match:
        return {}
    data: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        key_match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if key_match and not raw_line.startswith(" "):
            if current_key is not None:
                data[current_key] = "\n".join(current_lines).strip()
            current_key = key_match.group(1)
            value = key_match.group(2).strip()
            current_lines = [] if value in {">", ">-", "|", "|-"} else [value.strip("\"'")]
        elif current_key is not None:
            current_lines.append(line.strip())
    if current_key is not None:
        data[current_key] = "\n".join(current_lines).strip()
    return data


def tokenize(text: str) -> set[str]:
    normalized = re.sub(r"[`'\".,;:!?()\[\]{}\\/|，。：；、（）《》“”‘’]+", " ", text.lower())
    words = set()
    for token in normalized.split():
        token = token.strip()
        if len(token) < 2 or token in STOPWORDS:
            continue
        if len(token) <= 3 and token not in HIGH_VALUE_TERMS:
            continue
        words.add(token)
    return words


def load_skills(roots: Iterable[Path]) -> list[Skill]:
    skills: list[Skill] = []
    seen: set[tuple[str, str]] = set()
    for root in roots:
        if not root.exists():
            continue
        for child in sorted(root.iterdir()):
            skill_file = child / "SKILL.md"
            if not child.is_dir() or not skill_file.exists():
                continue
            meta = extract_frontmatter(skill_file.read_text(encoding="utf-8", errors="replace"))
            name = meta.get("name") or child.name
            description = meta.get("description", "")
            key = (child.name, name)
            if key in seen:
                continue
            seen.add(key)
            skills.append(Skill(root, child.name, name, description, skill_file))
    return skills


def score_overlap(query_name: str, query_text: str, skill: Skill) -> tuple[float, list[str]]:
    query_tokens = tokenize(f"{query_name} {query_text}")
    skill_tokens = tokenize(f"{skill.name} {skill.directory} {skill.description}")
    if not query_tokens or not skill_tokens:
        return 0.0, []
    common = sorted(query_tokens & skill_tokens)
    union = query_tokens | skill_tokens
    score = len(common) / len(union)
    bonus = 0.0
    if query_name and query_name.lower() in {skill.name.lower(), skill.directory.lower()}:
        bonus += 0.5
    bonus += min(0.2, 0.03 * len([term for term in common if term in HIGH_VALUE_TERMS]))
    return score + bonus, common


def default_roots() -> list[Path]:
    configured = os.environ.get("SKILLS_ROOT") or os.environ.get("AGENT_SKILLS_DIR")
    if configured:
        return [Path(os.path.expanduser(configured))]
    return [Path.cwd()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit skill overlap.")
    parser.add_argument("--name", default="", help="Proposed skill name.")
    parser.add_argument("--description", default="", help="Proposed skill description.")
    parser.add_argument("--intent", default="", help="Plain-language user intent for the proposed skill.")
    parser.add_argument("--roots", nargs="*", default=None, help="Skill roots to scan.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum overlaps to show.")
    args = parser.parse_args()

    roots = [Path(os.path.expanduser(p)) for p in args.roots] if args.roots else default_roots()
    query_text = " ".join(part for part in [args.intent, args.description] if part).strip()
    if not query_text and not args.name:
        parser.error("provide --intent, --description, or --name")

    skills = load_skills(roots)
    rows = []
    for skill in skills:
        if args.name and args.name.lower() in {skill.name.lower(), skill.directory.lower()}:
            continue
        score, common = score_overlap(args.name, query_text, skill)
        if score >= 0.08 or len(common) >= 3:
            rows.append((score, common, skill))
    rows.sort(key=lambda item: (item[0], len(item[1])), reverse=True)

    print("Skill overlap audit")
    print(f"Scanned roots: {', '.join(str(root) for root in roots)}")
    print(f"Scanned skills: {len(skills)}")
    print(f"Query: {(args.name + ' ' + query_text).strip()}")
    print()

    if not rows:
        print("No strong overlaps found.")
        print("Recommendation: creating a new bounded skill is reasonable if the intent is still distinct.")
        return 0

    print("Potential overlaps:")
    for score, common, skill in rows[: args.limit]:
        terms = ", ".join(common[:12]) if common else "name similarity"
        print(f"- {skill.directory} ({skill.name}) score={score:.2f}")
        print(f"  shared: {terms}")
        print(f"  path: {skill.path}")

    print()
    print("Recommended next action:")
    top_score = rows[0][0]
    top_common = rows[0][1]
    top_high_value = [term for term in top_common if term in HIGH_VALUE_TERMS]
    if top_score >= 0.25 or len(top_high_value) >= 3 or len(top_common) >= 4:
        print("Modify an existing skill unless the new skill has a clearly narrower boundary.")
    else:
        print("Creating a new skill may be reasonable, but add Do not use / Prefer / Defer to boundaries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
