# Skill Overlap Manager

> An agent skill for checking skill overlap before creating or changing local skills.

[中文 README](README.zh.md) · English

Skill Overlap Manager helps keep a growing skill collection understandable. Before a new skill is created, installed, or modified, it checks whether similar skills already exist and helps decide whether to update an existing skill or create a new one with a clearer scope.

---

## What It Does

- Finds existing skills with similar names, trigger terms, domains, or responsibilities.
- Highlights likely overlap between broad skills and more specific skills.
- Helps classify skills as primary workflows, tool operations, style layers, governance skills, or knowledge layers.
- Recommends whether to modify an existing skill, continue with a narrower new skill, archive an old skill, or cancel.
- Encourages clearer `Use when`, `Do not use when`, `Prefer`, `Defer to`, and `Pair with` boundaries in skill descriptions.

---

## Why It Exists

As local skills accumulate, repeated triggers like `write`, `polish`, `frontend`, `design`, `PPT`, or `debug` can make skill selection noisy. A new skill may duplicate an existing one, or a generic skill may compete with a more specific workflow.

This skill adds a preflight step: inspect what already exists before adding more.

---

## Core Workflow

```text
Inspect -> Compare -> Recommend -> Bound
```

- `Inspect`: Understand the skill the user wants to create or change.
- `Compare`: Scan existing skills for similar names, descriptions, and trigger terms.
- `Recommend`: Suggest whether to modify, create, archive, delete, or cancel.
- `Bound`: If the change proceeds, define a clearer scope for the skill.

---

## Install

This is a single-skill repository. The repository root is the skill root.

Required shape:

```text
skill-overlap-manager/
└── SKILL.md
```

### 1. Clone

```bash
git clone https://github.com/chemny/skill-overlap-manager.git
```

### 2. Place It In Your Agent's Skills Directory

Copy or symlink the cloned directory into the skills directory used by your agent.

### 3. Start A Fresh Agent Session

Many agents scan skill metadata when a new session starts. After installing, open a fresh session so the agent can read `SKILL.md`.

### 4. Verify

Try a prompt like:

```text
I want to create a new skill for SEO writing. First check whether I already have something similar.
```

### Update

If installed with Git:

```bash
git pull
```

---

## Usage Examples

```text
I want to create a new skill for Chinese AI tutorial writing. Check whether it overlaps with my existing skills.
```

```text
Help me improve the description of this skill and make sure it does not conflict with nearby writing skills.
```

```text
Before I install this presentation skill, check whether it overlaps with my current PPT or slides skills.
```

---

## Safety Boundaries

This skill is for skill overlap review and scope management. It should not:

- store secrets, tokens, cookies, or credentials,
- automatically delete existing skills,
- publish or push GitHub repositories,
- modify existing skills without user confirmation,
- put machine-specific operating policy into skill content.

---

## Repository Structure

```text
skill-overlap-manager/
├── SKILL.md
├── README.md
├── README.zh.md
├── LICENSE
└── scripts/
    └── audit_skill_overlap.py
```

---

## License

MIT
