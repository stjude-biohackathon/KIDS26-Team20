# Turing Way Repository Healthcheck

Reviewed: 2026-09-18

## Scope reviewed

Whole-repository review of the public
`stjude-biohackathon/KIDS26-Team20` repository at commit
`97c9048db38f855450c5a2e42c8c0186eba1e9b9` on `main`.

The project is a Python MCP learning-assistant server with agent skills, a
committed offline source snapshot, Docker/Compose deployment material, and a
MyGPT backend and data tree. Generated, vendored, binary, model, and large data
artifacts were excluded from code-quality and testing coverage assessment,
except when relevant to reproducibility or licensing.

Categories scored: version control and collaborative review; reproducible
computational environments; testing; continuous integration; code quality:
style and static analysis; code documentation; licensing and open code; and
community and stakeholder management.

## Overall score and confidence

**38 / 65 raw points (58%), Medium confidence.**

The repository has a strong documented and locked local setup, broad offline
tests, helpful layered documentation, and active multi-contributor Git history.
The combined quality check could not run because `uv` is unavailable in the
review environment. The public tree exposes only GitHub-managed Copilot
workflows, not a repository-controlled workflow that runs tests, linting, and
formatting on project changes.

## Rubric summary

| Category | Score | Maturity level | Rationale |
| --- | ---: | --- | --- |
| Version control and collaborative review | 7.5 / 10.0 | Strong | Recent scoped commits and repeated merged pull requests show an active, hosted collaboration workflow; universal recorded peer review cannot be confirmed. |
| Reproducible computational environments | 7.5 / 10.0 | Strong | `uv.lock`, documented frozen setup, a Dockerfile, and Compose provide versioned, portable setup paths. |
| Testing | 4.0 / 5.0 | Strong | The pytest suite covers normal and invalid-input behavior, supply-chain checks, and skill contracts, but it could not be executed in this environment. |
| Continuous integration | 0.0 / 5.0 | Missing | No tracked workflow runs the repository's formatting, linting, tests, or skill validation. |
| Code quality: style and static analysis | 5.0 / 10.0 | Developing | Ruff formatting and lint rules are configured and included in one local check command, but neither a passing run nor automatic enforcement was available. |
| Code documentation | 7.5 / 10.0 | Strong | README, contributor setup, Docker guidance, docstrings, and focused comments support users and developers. |
| Licensing and open code | 5.0 / 10.0 | Developing | A root MIT license is present, but the licenses and provenance boundaries of bundled third-party backend, model, and data artifacts are not separately documented. |
| Community and stakeholder management | 1.0 / 5.0 | Initial | Intended users, contributors, a Slack channel, onboarding, and recent activity are documented; the team role template is incomplete and no repository Code of Conduct exists. |

## Detailed evidence

### Project Design checklist

- Present: The README identifies the problem, inputs, expected output, tools,
  vision, mission, intended users, and a three-day roadmap.
  (`README.md:11-20`, `README.md:127-135`.)
- Present: The project has a public contribution path, offline check command,
  and source and credential boundaries. (`CONTRIBUTING.md:13-76`.)
- Partly present: `project-management/team.md` names participants and the Slack
  channel, but its team name, lead, project question, stack, roles, and
  responsibilities remain placeholders. (`project-management/team.md:3-24`.)
- Partly present: `project-management/project-plan.md` is an unfilled template
  for goal, tools, tasks, milestones, definition of done, and risks.
  (`project-management/project-plan.md:3-31`.)
- Incomplete: No release, archival, or final handoff plan was identified in the
  tracked project-management documentation.

### Version control and collaborative review: 7.5 / 10.0

Applied rubric cell: **Strong**. Changes are captured as meaningful,
well-messaged commits, and pull or merge requests are the normal integration
path.

- The public commit history at the reviewed revision includes recent merge pull
  requests and scoped commits from multiple contributors, for example the
  merges for pull requests 9, 10, 11, and 12 and commits headed `fix:` and
  `feat:`. (`https://github.com/stjude-biohackathon/KIDS26-Team20/commits/97c9048db38f855450c5a2e42c8c0186eba1e9b9`.)
- The team checklist specifies focused branches and commits, pull requests,
  peer review before merge, and recording checks.
  (`project-management/CHECKLIST.md:42-67`.)
- The public review cannot establish that every non-trivial change has a
  recorded peer review or that branch protection requires it. Exemplary was
  therefore not awarded.

### Reproducible computational environments: 7.5 / 10.0

Applied rubric cell: **Strong**. The environment is captured in portable,
versioned artifacts that a new contributor can use with minimal manual steps.

- `pyproject.toml` declares Python compatibility, application and development
  dependencies, pytest settings, and Ruff settings. `uv.lock` records the
  resolved Python environment. (`pyproject.toml:1-36`, `uv.lock`.)
- The supported setup uses `uv sync --extra dev --frozen`; the setup guide says
  that `--frozen` keeps contributors on the same reviewed dependency set.
  (`docs/SETUP.md:49-68`.)
- `Dockerfile` uses Python 3.12 and `uv sync --frozen`; `compose.yaml` defines
  the local multi-service stack, health checks, loopback ports, and persistent
  volumes. (`Dockerfile:1-29`, `compose.yaml:1-89`.)
- A clean-machine setup and full Docker bootstrap were not run. The fully
  demonstrated end-to-end reproduction required for Exemplary was not shown.

### Testing: 4.0 / 5.0

Applied rubric cell: **Strong**. Tests cover normal and failure or edge-case
behavior, run repeatably, and provide a fail-fast regression safety net.

- Pytest is configured with `tests` as the test path and automatic asyncio mode.
  (`pyproject.toml:27-36`.)
- `tests/test_mcp.py` exercises the in-memory MCP contract and invalid review
  inputs; `tests/test_supply_chain.py` covers lockfile integrity, exact build
  pins, no floating package execution, and commit-pinned corpus sources.
- Container tests verify loopback binding, pinned upstream MyGPT revision,
  provider-setting boundaries, and bootstrap provenance.
  (`tests/test_container.py:20-84`.)
- Contributors are instructed to keep default tests offline and deterministic,
  with live tests behind an explicit integration marker.
  (`CONTRIBUTING.md:20-27`.)
- The suite was not run because the `uv` command is unavailable. Automatic test
  execution was also not established, so Exemplary was not awarded.

### Continuous integration: 0.0 / 5.0

Applied rubric cell: **Missing**. No project CI is configured to run automated
checks on commits or pull requests.

- The complete public tree at the reviewed revision contains no tracked
  `.github/workflows` directory or workflow YAML file. The GitHub Actions API
  lists only GitHub-managed Copilot workflows, not a repository workflow that
  runs `scripts/project.py check`.
- `scripts/project.py` provides a sound local aggregate check, running Ruff
  format checking, Ruff linting, pytest, and skill validation.
  (`scripts/project.py:31-38`.) It is not connected to a tracked CI trigger.

### Code quality: style and static analysis: 5.0 / 10.0

Applied rubric cell: **Developing**. A linter is configured, but regular,
automatically enforced successful execution is not observable.

- Ruff has a 100-character line length, Python 3.11 target, and E/F/I/UP/B/SIM
  lint selections. (`pyproject.toml:38-45`.)
- The local aggregate check invokes `ruff format --check .` and `ruff check .`.
  (`scripts/project.py:31-38`.)
- Source modules use annotations, module docstrings, and focused helpers; for
  example, the review renderer validates exact score areas and evidence before
  emitting a report. (`src/learning_assistant/server.py:37-153`.)
- No tracked CI or pre-commit configuration runs the configured checks. The
  local command exited `127` because `uv` is not installed, so a clean result
  could not be observed.

### Code documentation: 7.5 / 10.0

Applied rubric cell: **Strong**. README, inline comments, and docstrings or API
documentation allow users and future developers to understand and extend the
project.

- `README.md` explains the project purpose, data boundary, stack, local setup,
  Docker bootstrap, MCP tools, roadmap, and contributor checks.
- `START_HERE.md`, `docs/SETUP.md`, and `docs/DOCKER.md` provide progressive
  onboarding for contributors and deployment users.
- Source and script modules include concise module and function docstrings;
  non-obvious package-install handling is also commented.
  (`scripts/project.py:1-24`, `src/learning_assistant/server.py:1-90`.)
- The project profile and team-management documentation retain placeholders,
  and there is no generated API reference. Exemplary was not awarded.

### Licensing and open code: 5.0 / 10.0

Applied rubric cell: **Developing**. A project-root license is present, but the
reuse terms for bundled third-party components are not distinguished.

- `LICENSE.md` is the standard MIT license, and the README identifies the
  project license. (`LICENSE.md:1-21`, `README.md:184-197`.)
- Contribution guidance requires source ownership, access, and license review
  before enabling institutional content. (`CONTRIBUTING.md:66-75`.)
- The repository includes `MyGPT_backend/`, committed model/data artifacts, and
  a separately pinned upstream MyGPT build source; a third-party notices file
  or per-component license inventory was not identified.
- This is below Strong because a reader cannot determine which root license
  applies to each bundled component.

### Community and stakeholder management: 1.0 / 5.0

Applied rubric cell: **Initial**. The project identifies contributors and
communication paths, but does not satisfy the next discrete level's required
project Code of Conduct and complete role documentation.

- The README identifies a broad set of intended user groups and names project
  contributors. (`README.md:11-20`, `README.md:29-40`.)
- The contribution guide and team checklist provide a newcomer path. The team
  file provides a Slack channel. (`CONTRIBUTING.md:1-76`,
  `project-management/CHECKLIST.md:42-67`, `project-management/team.md:3-26`.)
- Recent activity spans several named contributors and merged pull requests,
  demonstrating an active project rather than a stale repository.
- The complete recursive public tree contains no `CODE_OF_CONDUCT` file, and
  `project-management/team.md` still has unfilled lead and role fields. Under
  the rubric's discrete levels, Developing cannot be awarded.

## Checks run

| Command | Exit status | Result |
| --- | ---: | --- |
| `git log --format='%h %ad %an <%ae>%n%s' --date=short -30` | 0 | The local checkout showed recent activity, merge commits, scoped commit messages, and multiple contributors. |
| `uv run python scripts/project.py check` | 127 | Not run: `zsh: command not found: uv`. Dependencies were not installed or modified during this review. |

## Prioritized improvements

1. Add a tracked GitHub Actions workflow that runs `uv sync --extra dev --frozen`
   and `uv run python scripts/project.py check` on pushes and pull requests.
   This closes the CI gap and enforces the existing formatting, linting, tests,
   and skill validation.
2. Add a root `CODE_OF_CONDUCT.md`, assign a reporting contact and ownership,
   and link it from the README and contribution guide.
3. Complete `project-management/team.md` and `project-management/project-plan.md`
   with the accountable lead, roles, decision process, milestones, risks, and
   handoff/archive plan.
4. Add a third-party notices and provenance document for `MyGPT_backend/` and
   bundled model/data artifacts, clearly separating their reuse terms from the
   root MIT license.
5. Run the documented offline check from a supported clean environment and
   retain its result in pull-request or release evidence.

## The Turing Way sources

These are public guidance from The Turing Way, not St. Jude policy or a formal
certification. The rubric and source map are pinned in
`.agents/skills/turing-healthcheck-prototype/references/rubric.md`.

| Categories | Source |
| --- | --- |
| Project Design checklist; community | [Project Design Overview](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/project-design/pd-overview.md) |
| Version control and collaborative review | [Version Control](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/vcs.md), [Code Review](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/reviewing.md) |
| Reproducible computational environments | [Reproducible Environments](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/renv.md) |
| Testing | [Testing](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/testing.md) |
| Continuous integration | [Continuous Integration](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/ci.md) |
| Code quality | [Code Quality](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/code-quality.md) |
| Documentation | [Code Documentation](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/code-documentation.md), [Code Reuse](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/code-reuse.md) |
| Licensing and open code | [Licensing](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/licensing.md), [Open Research](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/open.md) |
| Community and stakeholder management | [Stakeholders: Personas and Pathways](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/project-design/stakeholders/persona.md), [Code of Conduct](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/community-handbook/coc.md), [Contributing](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/community-handbook/contributing.md), [Guide for Collaboration](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/collaboration/collaboration.md) |

## Limitations

- This is a transparent rubric-based healthcheck, not an official Turing Way
  certification, security audit, legal review, clinical assessment, or
  institutional-policy evaluation.
- The assessment targets the public `main` revision
  `97c9048db38f855450c5a2e42c8c0186eba1e9b9`. Local checkout differences were
  not used to lower the public repository score.
- `uv` is unavailable in the review environment. Formatting, linting, tests,
  and skill validation were not executed, and this report does not claim they
  pass.
- Generated, vendored, model, and data material was not reviewed for code
  correctness or test coverage. Its licensing boundary was included because it
  affects reuse.
