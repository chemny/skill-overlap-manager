---
name: skill-overlap-manager
description: Manage overlap between local agent skills. Use before creating, installing, modifying, optimizing, or deleting any user-managed skill. It scans existing skills for similar names, overlapping triggers, duplicated domains, unclear responsibilities, and missing metadata, then recommends whether to modify an existing skill, create a new clearly scoped skill, archive or delete an old skill, or cancel.
version: 0.1.0
metadata:
  short-description: Check skill overlap before creating or changing skills
---

# Skill Overlap Manager

Use this skill as a preflight gate before creating, installing, modifying, optimizing, or deleting user-managed skills.

This skill does not define machine-specific installation paths or workspace policy. Those are host-level operating rules and should live in the user's agent instruction files, not in this skill.

## Core Workflow

Before creating or installing a skill:

1. Capture the proposed skill intent.
2. Scan the existing skill inventory.
3. Identify similar or conflicting skills.
4. Tell the user what already exists and why it may overlap.
5. Recommend one of four actions:
   - Modify an existing skill.
   - Continue creating a new skill, but narrow its scope.
   - Archive or delete an obsolete skill.
   - Cancel the change.
6. Wait for confirmation before changing skill files unless the user has explicitly asked to execute a specific change.

Before modifying an existing skill:

1. Scan nearby skills in the same domain.
2. Check whether the proposed change broadens the skill's trigger surface.
3. Preserve a clear boundary between primary workflow skills, tool skills, style-layer skills, and governance skills.
4. Update the description only when it improves routing accuracy.

Before deleting or archiving a skill:

1. Confirm the exact directory name.
2. Check whether another skill depends on it or references it.
3. Ask for explicit confirmation before removal.

## Skill Types

Classify the proposed skill before judging overlap:

- `primary-workflow`: Owns an end-to-end task flow, such as writing a blog post, building a frontend, auditing security, or managing a Lark document.
- `tool-operation`: Wraps a tool or file format, such as FFmpeg, PDF, PPTX, DOCX, browser automation, or spreadsheet work.
- `style-layer`: Adds voice, brand, formatting, or editorial judgment on top of another workflow.
- `governance`: Audits, manages, tests, or improves other skills or agent behavior.
- `knowledge-layer`: Provides memory, reference material, ontology, or domain context.

When skills overlap, prefer the more specific primary workflow or tool-operation skill as the main handler. Use style-layer skills only as companions unless the user's request is specifically about style.

## Conflict Signals

Treat these as potential conflicts:

- Similar names or aliases.
- Shared high-value triggers such as `write`, `polish`, `article`, `frontend`, `design`, `PPT`, `Feishu`, `Lark`, `PDF`, `test`, or `debug`.
- Same domain and same task stage.
- One generic skill and one more specific skill both claim the same user request.
- A new skill's description contains broad keywords already owned by existing specialized skills.
- A skill claims host-level operating rules, such as machine-specific paths or workspace policy, instead of local workflow rules.

Overlapping words are not automatically bad. A conflict matters when two skills would both try to be the primary workflow for the same request.

## Boundary Language

When a new skill is still warranted, write scope boundaries directly into the description and body:

- `Use when`: The precise user intent and artifacts this skill owns.
- `Do not use when`: Similar requests that should belong to another skill.
- `Prefer`: Which skill wins when both could apply.
- `Defer to`: Skills that should own adjacent workflows.
- `Pair with`: Skills that can be used together without competing.

Avoid descriptions that only pile up keywords. A good description is a routing contract.

## User Prompt Template

When overlaps are found, use this shape:

```text
I found similar skills already installed:

- <skill>: <why it overlaps>
- <skill>: <why it overlaps>

Recommendation: <modify existing / create new with narrower boundary / archive old / cancel>.

Options:
1. Modify an existing skill.
2. Continue creating a new skill, but define clear Do not use / Prefer / Defer to rules.
3. Archive or delete an old skill first.
4. Cancel.
```

Keep the recommendation direct. Ask only when the choice materially changes which files will be changed.

## Audit Script

Use `scripts/audit_skill_overlap.py` to scan local skill folders and compare a proposed skill against the current inventory.

Examples:

```bash
python3 scripts/audit_skill_overlap.py --intent "Create a skill for Chinese AI tutorial writing style"
python3 scripts/audit_skill_overlap.py --name neo-writing-style --description "Use when writing Chinese AI tutorials in Neo's voice"
python3 scripts/audit_skill_overlap.py --roots /path/to/skills --intent "Install a PDF processing skill"
```

The script produces a concise text report with likely overlaps, shared trigger terms, and recommended next actions.
