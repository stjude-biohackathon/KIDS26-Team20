# Turing Way-Aligned Readiness Snapshot

> **This is not an official certification.** The Turing Way is public best-practice
> guidance, not a certifying authority. This document is a transparent,
> evidence-based readiness snapshot of observable repository practices against a
> ten-criterion rubric inspired by The Turing Way. It carries no legal, institutional,
> or academic certification weight.

- **Repository reviewed:** [`stjude-biohackathon/KIDS25-Team9`](https://github.com/stjude-biohackathon/KIDS25-Team9)
- **Commit reviewed:** `275a38b5c3f1062564cb742a9b7daecf1130287b` (branch `main`)
- **Review date:** 2026-09-18
- **Scope:** Public repository root, `src/` tree, git history, issues, branches, and repository metadata (README, LICENSE, `pyproject.toml`, `.github`, tests). No private data, credentials, or restricted files were accessed.
- **Confidence:** Medium-high. Findings are based on direct inspection of the repository tree and GitHub metadata (issues, branches, contents API) at the commit above; no CI logs, releases, or private discussions exist to review.

## Total score: 22 / 100

| # | Criterion | Score (/10) | Observed evidence |
|---|-----------|:-----------:|--------------------|
| 1 | Project purpose and scope | 4 | [README.md](https://github.com/stjude-biohackathon/KIDS25-Team9/blob/275a38b5c3f1062564cb742a9b7daecf1130287b/README.md) states a clear purpose (napari plugin for DL image analysis) and lists supported tasks (2D/3D U-Net, Mask R-CNN, Faster R-CNN), but there is no explicit intended-audience statement or documented known limitations beyond a one-line "Transformer networks incoming" note. |
| 2 | Version control and provenance | 4 | 37 commits from 6 contributors with merged PRs (e.g. [PR #11](https://github.com/stjude-biohackathon/KIDS25-Team9/pull/11)), but no git tags/releases, no CHANGELOG, several non-descriptive commit messages (e.g. `"May the force be with us !"` x3), and 20 compiled `__pycache__/*.pyc` files are tracked in git with [no root-level `.gitignore`](https://github.com/stjude-biohackathon/KIDS25-Team9/tree/275a38b5c3f1062564cb742a9b7daecf1130287b/src). |
| 3 | Open collaboration | 3 | GitHub Issues are enabled and actively used (4 open issues, e.g. [#27](https://github.com/stjude-biohackathon/KIDS25-Team9/issues/27), [#25](https://github.com/stjude-biohackathon/KIDS25-Team9/issues/25)) and 14 feature branches show active collaboration, but there is [no `CONTRIBUTING.md` or `CODE_OF_CONDUCT.md`](https://github.com/stjude-biohackathon/KIDS25-Team9/tree/275a38b5c3f1062564cb742a9b7daecf1130287b) anywhere in the tree, and no maintainer/PR-review guidance is documented. |
| 4 | Reproducible environments | 2 | [`pyproject.toml`](https://github.com/stjude-biohackathon/KIDS25-Team9/blob/275a38b5c3f1062564cb742a9b7daecf1130287b/pyproject.toml) defines build metadata and a napari entry point, but declares **no `[project].dependencies`**, and no `requirements.txt`, `environment.yml`, lock file, or Dockerfile exists to pin the runtime environment. |
| 5 | Data and workflow provenance | 2 | Model configuration files exist (`maskrcnn_config.json`, `src/configs/*/config.json`), but there is no documentation of data sources, expected data schemas/formats, or workflow steps connecting annotation → training → inference. |
| 6 | Testing and validation | 0 | No file or directory matching a test suite (`tests/`, `test_*.py`, `pytest`, etc.) exists anywhere in the repository tree. |
| 7 | Automation and continuous integration | 0 | The repository has no `.github` directory; `GET /repos/stjude-biohackathon/KIDS25-Team9/contents/.github` returns `404 Not Found`. No CI workflow of any kind runs on commits or pull requests. |
| 8 | Documentation and usability | 3 | README clearly lists features and supported architectures, but has no installation instructions, no usage/quickstart example, and no developer documentation; the GitHub Wiki is enabled but the repository description/topics are empty. |
| 9 | Licensing, attribution, and responsible reuse | 4 | An [MIT `LICENSE`](https://github.com/stjude-biohackathon/KIDS25-Team9/blob/275a38b5c3f1062564cb742a9b7daecf1130287b/LICENSE) is present at the root, but there is no `CITATION.cff`, no third-party attribution notes, and no explicit reuse/citation guidance for downstream users. |
| 10 | Ethics, accessibility, and sustainability | 0 | No ethics, accessibility, or sustainability/maintenance statement exists anywhere in the repository; no archival plan (e.g. Zenodo/DOI integration) is present. |

## Checks performed

- Listed and read all root-level files (`README.md`, `LICENSE`, `pyproject.toml`, `maskrcnn_config.json`) and the full `src/` tree.
- Searched the repository for `CONTRIBUTING*`, `CODE_OF_CONDUCT*`, `CITATION.cff`, `*requirements*`, `*environment*`, and `test*` files — none found.
- Queried the GitHub REST API for repository metadata, branches, contributors, open issues, `.github` contents, tags, and releases.
- Inspected `git log` (37 commits, 6 named contributors) and confirmed 20 tracked `__pycache__/*.pyc` files with no root `.gitignore`.
- Retrieved grounding guidance from The Turing Way's book via the learning-assistant RAG tool (`turing-way` dataset, relevance score 89.0) for all ten criteria before scoring.

## Recommendations (pinned to Turing Way guidance)

| # | Recommendation | Repository evidence | Turing Way source |
|---|-----------------|----------------------|--------------------|
| 1 | Add automated tests (unit/integration); no test files exist anywhere in the repository, so regressions cannot be caught before merge. | No `tests/`/`test_*` layout found in the [repository tree](https://github.com/stjude-biohackathon/KIDS25-Team9/tree/275a38b5c3f1062564cb742a9b7daecf1130287b). | [Testing Resources](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-resources.md) |
| 2 | Add a CI workflow (e.g. GitHub Actions) to run tests and checks automatically on each push/PR. | No `.github` directory exists at the reviewed commit ([tree](https://github.com/stjude-biohackathon/KIDS25-Team9/tree/275a38b5c3f1062564cb742a9b7daecf1130287b)); the contents API returns 404 for `.github`. | [Continuous Integration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md) |
| 3 | Declare and pin project dependencies in `pyproject.toml` and/or add an environment/requirements/lock file. | [`pyproject.toml`](https://github.com/stjude-biohackathon/KIDS25-Team9/blob/275a38b5c3f1062564cb742a9b7daecf1130287b/pyproject.toml) has no `[project].dependencies`, and no requirements/environment/lock file exists. | [Reproducible Environments overview](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/overview/overview-benefit.md) |
| 4 | Add `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` to formalize open collaboration norms. | No such files exist at the [repository root or elsewhere](https://github.com/stjude-biohackathon/KIDS25-Team9/tree/275a38b5c3f1062564cb742a9b7daecf1130287b), though 4 open issues and 14 branches show active but informal collaboration. | [Project Repository Participation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/pd-overview/project-repo/project-repo-participation.md) |
| 5 | Add a `CITATION.cff` file so the software and its contributors can be formally cited and credited. | No `CITATION.cff` exists despite the [MIT LICENSE](https://github.com/stjude-biohackathon/KIDS25-Team9/blob/275a38b5c3f1062564cb742a9b7daecf1130287b/LICENSE) being present. | [Citation File Format (CFF)](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/communication/citable/citable-cff.md) |

## Limitations

- This snapshot reflects only the single commit reviewed (`275a38b5`); the repository has many active feature branches not evaluated.
- No repository maintainer was consulted; internal practices (e.g. informal code review over chat, undocumented CI run elsewhere) may exist but are not observable from the public repository alone.
- Scores are evidence-gated: a criterion scores 0 only when no reliable evidence was found in the reviewed scope, not as a judgment of the team's actual practices.
- This is a readiness snapshot for improvement planning, **not** an official Turing Way, institutional, or legal certification of any kind.
