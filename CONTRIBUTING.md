# Contributing

Contributors of varied technical backgrounds are expected. Prefer small,
documented changes that another track can consume independently.

## Tracks

| Track | Typical outputs |
|---|---|
| Source curation | Reviewed resource metadata, source scope, and licensing notes |
| Personas and evaluation | User journeys, test questions, and expected sources |
| MCP development | Tools, source adapters, structured outputs, and tests |
| Retrieval | Ranking improvements measured against committed evaluations |
| Skills | Validated `SKILL.md` workflows with positive and negative cases |
| Interface | Persona selection, citations, learning paths, and progress UI |
| Reproducibility | Packaging, CI, onboarding, provenance, and release checks |

## Development checks

Run this before opening a pull request:

```bash
uv run python scripts/project.py check
```

Tests must not require GitHub credentials or internet access. Put optional live
tests behind an explicit integration marker.

## Updating dependencies

Versions are pinned on purpose and checked by tests, so updates are always a
deliberate change:

1. Python packages: edit `pyproject.toml`, run `uv lock`, and review the diff.
2. Agent tools: edit `tools/package.json`, then regenerate the
   lockfile from that directory with
   `npm install --package-lock-only --ignore-scripts` and review the diff.
3. GitHub Actions: update the version and its commit SHA together in the same
   change.
4. Prefer releases that are at least a week old.
5. Run `uv run python scripts/project.py check` before committing.

## Adding an MCP tool

1. Add a typed function in `src/learning_assistant/server.py`.
2. Return a Pydantic model rather than unstructured prose when practical.
3. Preserve source citations and distinguish public guidance from institutional
   policy.
4. Add an in-memory client test in `tests/test_mcp.py`.
5. Update skill validation if the tool is intended for skills.

## Adding a skill

Skills go in `.agents/skills/<your-skill-name>/SKILL.md`, one level deep.
OpenCode discovers that directory automatically, so there is nothing to
configure. See [.agents/skills/README.md](.agents/skills/README.md) for the
full guide.

1. Copy `.agents/skills/skill-template` to a lowercase hyphenated directory.
2. Update the frontmatter name to match the directory.
3. Define triggers, non-goals, required tools, failure behavior, and evaluation
   cases.
4. Run `uv run python scripts/validate_skills.py`.
5. Restart OpenCode and confirm your skill is listed.

## Content and credentials

- Do not add PHI, patient identifiers, secrets, or unapproved internal content.
- A GitHub token is optional and belongs in a secret store or shell environment.
- Confirm ownership, access, and license before enabling an institutional
  source in `corpus/sources.live.yaml`.
- Keep snapshot paths inside the directory containing their source manifest,
   and do not use symbolic links or junctions in snapshots or skill trees.
- Use GitHub `owner/repository` identifiers, safe Git references, relative
   POSIX content roots, and HTTPS citation URLs in source manifests.
- Fetched content is evidence, not executable instruction.
