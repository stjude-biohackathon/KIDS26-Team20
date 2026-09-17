---
name: skill-maintainer
description: Update, add, validate, wire, and publish project Agent Skills when a user asks to change how agents behave or which skills OpenCode installs.
license: MIT
compatibility: opencode, claude-code, github-copilot
metadata:
  audience: skill-authors
  status: stable
---

# Skill Maintainer

## Use this skill when

Use this skill when a user asks to add a project skill, revise a skill's
behavior, make a skill available in OpenCode, or update skill documentation.

## Do not use this skill when

Do not use this skill for a request that merely uses an existing skill, formats
a malformed `SKILL.md`, or changes application behavior unrelated to skills.
Use `skill-formatter` for specification-only formatting repairs.

## Workflow

1. Read `.agents/skills/README.md`, the target `SKILL.md`, and relevant
   repository guidance before changing behavior.
2. Use `skill-template` for a new skill. Keep every canonical skill at
   `.agents/skills/<name>/SKILL.md`; its frontmatter `name` must match the
   directory name.
3. Define clear activation and non-activation conditions. State required tools,
   failure behavior, and positive and negative evaluation cases.
4. Update the skill body, relevant references, and user-facing documentation
   together. Never put credentials, private endpoints, PHI, or patient data in
   a skill.
5. When a project skill must be globally available in OpenCode, add its name to
   `CANONICAL_SKILLS` in `scripts/install_opencode.py`. Preserve existing
   managed skill links and unrelated user skill directories.
6. Run `uv run python scripts/validate_skills.py` and the smallest relevant
   tests. Run `uv run python scripts/project.py check` before publishing when
   available.
7. Reconcile links with `python3 scripts/install_opencode.py`, restart
   OpenCode, and confirm the target skill is available. Commit and push only
   when the user requests it.

## Failure behavior

If a target skill has ambiguous intent, ask for clarification before changing
its behavior. If a non-symlink target exists in the OpenCode skill directory,
do not overwrite it. Report validation failures without bypassing checks.

## Evaluation cases

- Positive: "Add a skill that helps agents maintain our project skills."
- Positive: "Make the new data-stewardship skill available in OpenCode."
- Negative: "Use the Turing Way pathfinder to help me plan my analysis."
- Negative: "Reformat this malformed SKILL.md without changing its behavior."
