# Skills

This directory is where every skill in the project lives, including yours.

Put your skill here:

```text
.agents/skills/<your-skill-name>/SKILL.md
```

That is the whole requirement. OpenCode discovers this directory on its own when
you launch it from the repository root, so there is no configuration file to
edit and no path to register. Restart OpenCode after adding a skill and it will
be available through the `skill` tool.

## The one rule that catches people out

Your skill must sit **exactly one level deep**, in its own directory, in a file
named `SKILL.md` in capitals.

```text
.agents/skills/citation-checker/SKILL.md          discovered
.agents/skills/my-team/citation-checker/SKILL.md  not discovered, nested too deep
.agents/skills/citation-checker/skill.md          not discovered, wrong filename
.agents/skills/citation-checker.md                not discovered, needs its own directory
```

Everyone's skills share this one flat directory. That is a constraint of how
OpenCode finds skills, not a filing decision, so please do not add grouping
subdirectories.

## Getting started

Copy the template and rename it:

```bash
cp -r .agents/skills/skill-template .agents/skills/your-skill-name
```

Windows (PowerShell):

```powershell
Copy-Item -Recurse .agents\skills\skill-template .agents\skills\your-skill-name
```

Then edit `SKILL.md`. The `name` in the frontmatter must match your directory
name exactly, using lowercase letters, digits, and single hyphens.

While your skill is still a draft, say so in the frontmatter so reviewers can
tell work in progress from the project's settled skills:

```yaml
metadata:
  status: draft
```

## What the validator requires

Run this before you commit:

```bash
uv run python scripts/validate_skills.py
```

It checks that every skill has:

- a `name` that is lowercase and hyphenated and matches its directory;
- a `description` between 1 and 1024 characters;
- the sections `## Use this skill when`, `## Do not use this skill when`, and
  `## Evaluation cases`;
- only real MCP tool names, if you reference any. The server is deliberately
  small and provides two: `learning-assistant_list_resources` and
  `learning-assistant_get_resource`. A typo here fails the build rather than
  failing silently at runtime. If your team adds a tool, add its name to
  `KNOWN_TOOLS` in `src/learning_assistant/skill_validation.py`.

It also refuses anything that looks like a credential or private key. Never put
an API key, a token, an internal endpoint, or patient data in a skill.

## Writing a skill that actually triggers

The `description` and the two "when" sections are what an agent reads to decide
whether to use your skill, so write them for that purpose:

- Describe the **user request** that should trigger it, not what the skill does
  internally.
- Use `## Do not use this skill when` to fence off adjacent requests that belong
  to a different workflow. This matters as much as the trigger.
- Give the workflow as numbered, concrete steps.
- Say what to do when something fails, and rule out inventing sources or
  citations.
- List at least one positive and one negative evaluation case, so the next
  person can tell whether a change broke your intent.

The `skill-template` skill shows these conventions in practice.

## Checking your work

```bash
# Validate the skills only
uv run python scripts/validate_skills.py

# Full pre-pull-request check: formatting, linting, tests, skills
uv run python scripts/project.py check

# Confirm the skills and the MCP server are wired up
uv run python scripts/project.py doctor
```

Then restart OpenCode, ask it to list its skills, and confirm yours appears.

See the contribution tracks in [CONTRIBUTING.md](../../CONTRIBUTING.md) and the
setup steps in [docs/SETUP.md](../../docs/SETUP.md).
