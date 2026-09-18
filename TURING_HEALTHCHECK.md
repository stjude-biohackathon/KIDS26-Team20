# Turing Healthcheck

Review date: 2026-09-17

## Scope Reviewed

Whole-repository review of the St. Jude AI and Data Learning Assistant at commit
`3de0c943a0d4ed021be9e744c5a26f7772497043`. The reviewed project is a Python
MCP service with local Docker services and pinned Node-based contributor tools.
Generated dependencies, Docker volumes, caches, binaries, and ignored local
configuration were excluded.

Rubric categories scored: Version control and collaborative review; reproducible
computational environments; testing; continuous integration; code quality:
style and static analysis; code documentation; licensing and open code; and
community and stakeholder management.

Project Design checklist evidence: the README records a project question, input
sources, expected output, stack, and a communication channel. The team/roles
template and the handoff section retain unresolved placeholders. The contribution
guidance documents version-control and review expectations. No completed archive
or post-project publishing plan was observed.

## Overall Score And Confidence

**48 / 65 (74%), medium confidence.**

Repository documentation and tracked configuration were inspected across every
scored category. The documented offline validation command could not run because
`uv` is not installed or on this review environment's `PATH`, so test, formatter,
lint, and skill-validation results could not be independently confirmed.

## Rubric Summary

| Category | Earned | Maximum | Maturity level | Rationale |
| --- | ---: | ---: | --- | --- |
| Version control and collaborative review | 7.5 | 10 | Strong | Meaningful commits and four recorded merge commits are present; project guidance expects focused branches, pull requests, and teammate review. |
| Reproducible computational environments | 10.0 | 10 | Exemplary | `uv.lock`, a pinned Dockerfile, Compose services, and documented clean-machine setup provide versioned, automated environment reconstruction. |
| Testing | 4.0 | 5 | Strong | Nine organized test modules cover normal and failure behavior, including MCP contracts, installation, container boundaries, and supply-chain rules. |
| Continuous integration | 0.0 | 5 | Missing | No workflow files exist under `.github/workflows`, so no automated repository CI was observable. |
| Code quality: style and static analysis | 7.5 | 10 | Strong | Ruff rules and formatting/lint commands are configured; the full check could not be run in this environment. |
| Code documentation | 7.5 | 10 | Strong | README, setup guides, contribution guidance, docstrings, and inline comments cover users and maintainers. |
| Licensing and open code | 7.5 | 10 | Strong | Root `LICENSE.md` supplies the standard MIT license and the README identifies it; bundled external-source licensing boundaries are described but not exhaustively mapped. |
| Community and stakeholder management | 2.5 | 5 | Developing | Contributor roles and a Slack channel are named, and the team checklist directs collaboration, but several project-specific roles and communication fields remain templates and the Code of Conduct is external rather than a tracked project file. |

## Detailed Evidence

### Version Control And Collaborative Review

- Observed: `git log --oneline -20` shows focused `feat:` and `fix:` commits; `git log --merges --oneline -20` shows four recorded pull-request merges.
- Observed: `project-management/CHECKLIST.md:45-60` requires a focused branch, a pull request, another teammate's review, and recorded checks or limitations.
- Rubric cell applied: **Strong (7.5/10)**, “Changes are captured as meaningful, well-messaged commits, and pull or merge requests are the norm, typically reviewed by at least one other contributor before merging.”

### Reproducible Computational Environments

- Observed: `pyproject.toml:1-24` declares Python compatibility and development dependencies; `uv.lock` is tracked.
- Observed: `Dockerfile:1-29` pins Python 3.12 and uv 0.11.8, installs with `uv sync --frozen`, and defines a health check.
- Observed: `compose.yaml:1-89` versions the local database, MyGPT backend commit, service dependencies, health checks, and local-only ports.
- Observed: `docs/SETUP.md:15-157` documents installation from a clean machine and pinned tool verification.
- Rubric cell applied: **Exemplary (10/10)**, “The full computational environment — dependencies, versions, and any needed services — is versioned, automated, and demonstrably reproducible from a clean machine.” The portable build and service setup were inspected; the documented check was not runnable here.

### Testing

- Observed: `tests/` contains nine test modules. `tests/test_mcp.py:40-73` exercises the in-memory MCP contract and offline source retrieval.
- Observed: `tests/test_container.py:20-84` checks loopback binding, pinned upstream revisions, secret isolation, and bootstrap configuration. `tests/test_supply_chain.py:19-88` checks lock integrity and immutable external source pins.
- Rubric cell applied: **Strong (4/5)**, “Tests cover both normal and failure or edge-case behavior, run repeatably, and act as a fail-fast safety net that catches regressions when code changes.”

### Continuous Integration

- Observed: `.github/` contains only `copilot-instructions.md`; no `.github/workflows` directory or workflow configuration was found in the tracked checkout.
- Rubric cell applied: **Missing (0/5)**, “No CI is configured; any tests that exist are only ever run manually by individuals.”

### Code Quality: Style And Static Analysis

- Observed: `pyproject.toml:38-43` configures Ruff formatting/linting with rules `E`, `F`, `I`, `UP`, `B`, and `SIM`.
- Observed: `scripts/project.py:34-38` makes `ruff format --check .` and `ruff check .` part of the documented check.
- Rubric cell applied: **Strong (7.5/10)**, “A linter or static analysis tool is configured and passes cleanly, or with justified exceptions, across most of the codebase, and style is consistent.” Passing output was not independently available.

### Code Documentation

- Observed: `README.md:11-25` describes the purpose, input sources, expected output, stack, and project roles; `README.md:35-110` documents local and Docker setup.
- Observed: `docs/SETUP.md:1-242` provides ordered onboarding, verification, failure guidance, and explicit credential boundaries.
- Observed: `scripts/project.py:1-24` and `tests/test_supply_chain.py:1-18` include docstrings and comments for non-obvious behavior.
- Rubric cell applied: **Strong (7.5/10)**, “A README, inline comments, and docstrings or API documentation together let both users and future developers understand what the code does, why, and how to use or extend it.”

### Licensing And Open Code

- Observed: `LICENSE.md:1-21` contains the MIT license; `README.md:195-197` links to it.
- Observed: `README.md:14-16` identifies the Turing Way corpus as CC-BY-4.0 and states that institutional resources are disabled pending ownership, scope, and license review.
- Rubric cell applied: **Strong (7.5/10)**, “A clear, standard license file, recognizable by hosting platforms such as GitHub or GitLab, is present, and it is reasonably clear what license applies to which part of the project.”

### Community And Stakeholder Management

- Observed: `README.md:13-20` identifies the intended audience, a team lead placeholder, team-role reference, and a Slack channel.
- Observed: `CONTRIBUTING.md:6-16` defines contribution tracks, while `project-management/CHECKLIST.md:42-60` documents the contributor workflow and review expectation.
- Observed limitation: `project-management/team.md:3-24` retains placeholders for team name, lead, problem, tools, roles, and responsibilities. `project-management/CHECKLIST.md:122-133` also retains communication placeholders; it links to an external Code of Conduct at lines 71-75 rather than including a repository `CODE_OF_CONDUCT` file.
- Rubric cell applied: **Developing (2.5/5)**, “Roles or stakeholder groups are documented ... and a `CODE_OF_CONDUCT` file is present, but there is no explicit persona/pathway analysis or onboarding guidance for newcomers.” This repository has documented roles, channels, contributor onboarding, and an external code-of-conduct reference, but the project-specific role and channel documentation is incomplete; the score does not assume the external document is a tracked code-of-conduct file.

## Checks Run

| Command | Exit status | Result |
| --- | ---: | --- |
| `git status --short --branch` | 0 | Working tree was clean on `rubric-review`, tracking `origin/rubric-review`. |
| `git log --oneline -20` | 0 | Recent history has meaningful, scoped commit messages. |
| `git log --merges --oneline -20` | 0 | Four recorded pull-request merge commits found. |
| `uv run python scripts/project.py check` | 127 | Not run: `uv` was not found on `PATH`. |

## Prioritized Improvements

1. Add a GitHub Actions workflow that runs the existing `uv run python scripts/project.py check` command on pushes and pull requests.
2. Complete `project-management/team.md` with real roles, responsibilities, ownership, and backup support, then complete the communication and check-in fields in the team checklist.
3. Add a repository `CODE_OF_CONDUCT.md` or clearly document the project adoption and accessible location of the existing event Code of Conduct.
4. Add CI enforcement for Ruff formatting and linting, preserving the existing single local check command as the common source of truth.
5. Run the documented check in a clean contributor environment and record its result in the pull request or project documentation; this confirms that the strong test and style claims hold in practice.

## The Turing Way Sources

These are public best-practice guidance from The Turing Way, not St. Jude policy or a certification.

| Area | Title | Repository | Path | Ref | URL |
| --- | --- | --- | --- | --- | --- |
| Project design and stakeholder management | Project Design Overview | the-turing-way/the-turing-way | `book/website/project-design/pd-overview.md` | `7b7c9a5904a4c9382933b74409ca0705439baa27` | https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/project-design/pd-overview.md |
| Version control and review | Version Control; Code Review | the-turing-way/the-turing-way | `book/website/reproducible-research/vcs.md`; `book/website/reproducible-research/reviewing.md` | `7b7c9a5904a4c9382933b74409ca0705439baa27` | https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/vcs.md ; https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/reviewing.md |
| Reproducible environments | Reproducible Environments | the-turing-way/the-turing-way | `book/website/reproducible-research/renv.md` | `7b7c9a5904a4c9382933b74409ca0705439baa27` | https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/renv.md |
| Testing | Testing | the-turing-way/the-turing-way | `book/website/reproducible-research/testing.md` | `7b7c9a5904a4c9382933b74409ca0705439baa27` | https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/testing.md |
| Continuous integration | Continuous Integration | the-turing-way/the-turing-way | `book/website/reproducible-research/ci.md` | `7b7c9a5904a4c9382933b74409ca0705439baa27` | https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/ci.md |
| Code quality | Code Quality | the-turing-way/the-turing-way | `book/website/reproducible-research/code-quality.md` | `7b7c9a5904a4c9382933b74409ca0705439baa27` | https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/code-quality.md |
| Documentation | Code Documentation; Code Reuse | the-turing-way/the-turing-way | `book/website/reproducible-research/code-documentation.md`; `book/website/reproducible-research/code-reuse.md` | `7b7c9a5904a4c9382933b74409ca0705439baa27` | https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/code-documentation.md ; https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/code-reuse.md |
| Licensing | Licensing; Open Research | the-turing-way/the-turing-way | `book/website/reproducible-research/licensing.md`; `book/website/reproducible-research/open.md` | `7b7c9a5904a4c9382933b74409ca0705439baa27` | https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/licensing.md ; https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/open.md |
| Community and stakeholder management | Stakeholders: Personas and Pathways; Code of Conduct; Contributing to The Turing Way; Guide for Collaboration | the-turing-way/the-turing-way | `book/website/project-design/stakeholders/persona.md`; `book/website/community-handbook/coc.md`; `book/website/community-handbook/contributing.md`; `book/website/collaboration/collaboration.md` | `7b7c9a5904a4c9382933b74409ca0705439baa27` | https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/project-design/stakeholders/persona.md ; https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/community-handbook/coc.md ; https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/community-handbook/contributing.md ; https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/collaboration/collaboration.md |

## Limitations

- This report evaluates visible repository practices, not security, legal compliance, clinical suitability, accessibility, performance, or institutional policy.
- `uv` was unavailable, so the repository's documented formatter, linter, test, and skill-validation command was not executed.
- Git history and merge commits demonstrate a review path but do not prove that every change received peer review.
- No live Turing Way retrieval was used for this prototype; citations are the skill rubric's pinned source map.
