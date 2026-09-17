# Turing Healthcheck Rubric

This rubric scores a codebase against seven practices from The Turing Way's
Reproducible Research guide, the handbook's chapters most directly about how
code is written, tested, and shared. It replaces earlier draft categories
(such as "performance" and "grammar") that were not grounded in a specific
Turing Way chapter.

Select exactly one maturity level per category from observable repository
evidence. Do not average adjacent levels or silently reweight categories.
Category points are the category weight multiplied by the listed maturity
fraction; report category points to one decimal place and round the final
total to the nearest whole number.

For a requested-change review, apply each description only to the requested
change. Use surrounding code as context and list pre-existing concerns without
deducting them from the change score.

## Version control and collaborative review (15 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | The code is not under version control, or its history does not show what changed, when, or by whom, and no review path exists for changes. |
| Initial | 3.75 | Code is under version control, but commit messages rarely explain why a change was made, unrelated changes are bundled together, and no pull or merge requests are used. |
| Developing | 7.5 | Commits are reasonably scoped and messaged on a hosted repository, but pull or merge requests and code review happen only occasionally, not as a habit. |
| Strong | 11.25 | Changes are captured as meaningful, well-messaged commits, and pull or merge requests are the norm, typically reviewed by at least one other contributor before merging. |
| Exemplary | 15 | History clearly documents what changed and why for every change, and every non-trivial change goes through recorded peer review before merging, in line with reviewing code as "an additional way of testing code quality." |

## Reproducible computational environments (15 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | Nothing in the repository identifies the runtime, language version, or dependencies, so another person cannot reconstruct the environment the code needs. |
| Initial | 3.75 | A dependency list exists (for example `requirements.txt` or `package.json`), but versions are unpinned or setup requires undocumented manual steps. |
| Developing | 7.5 | Dependencies are declared with pinned versions or a lockfile for the main workflow, but the environment itself is not captured in a portable, one-command form. |
| Strong | 11.25 | The environment is captured in a portable, versioned artifact (a lockfile plus documented setup, a Dockerfile, a conda environment file, or a Binder configuration) that a new contributor can use with minimal manual steps. |
| Exemplary | 15 | The full computational environment — dependencies, versions, and any needed services — is versioned, automated, and demonstrably reproducible from a clean machine, matching the guide's emphasis on "mobility of compute." |

## Testing (20 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | No automated tests exist; correctness depends on informal, undocumented manual checks. |
| Initial | 5 | Some ad hoc tests or scratch scripts exist, but they are not organized into a runnable test suite and are not repeatable. |
| Developing | 10 | Informal checks have been turned into functions collected in a test suite that covers the main happy path and can be run locally. |
| Strong | 15 | Tests cover both normal and failure or edge-case behavior, run repeatably, and act as a fail-fast safety net that catches regressions when code changes. |
| Exemplary | 20 | A maintained test suite covers critical behavior and edge cases, runs automatically, and gives clear, repeatable evidence that changes have not broken existing behavior. |

## Continuous integration (10 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | No CI is configured; any tests that exist are only ever run manually by individuals. |
| Initial | 2.5 | A CI configuration exists but is incomplete, is not actually triggered on commits or pull requests, or is frequently broken and ignored. |
| Developing | 5 | CI automatically runs the test suite on pushes or pull requests to the main branch, catching some regressions before merge. |
| Strong | 7.5 | CI runs on every commit or pull request, covers most of the test suite, and a failing run reliably blocks or flags problematic merges. |
| Exemplary | 10 | CI integrates changes frequently, runs the full test suite and related checks (such as linting) automatically, and a red CI run is treated as something to fix immediately, matching the guide's goal of finding bugs "early, minimizing their damage." |

## Code quality: style and static analysis (15 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | No consistent coding style is evident, and no linter or static analysis tool is configured or referenced anywhere in the project. |
| Initial | 3.75 | Some files follow a consistent style, but nothing enforces it, and inconsistency is common across the codebase. |
| Developing | 7.5 | A linter or static analysis tool (for example Pylint, ESLint, or shellcheck) is configured, but it is not run consistently and several flagged issues remain unresolved. |
| Strong | 11.25 | A linter or static analysis tool is configured and passes cleanly, or with justified exceptions, across most of the codebase, and style is consistent. |
| Exemplary | 15 | Static analysis and a consistent style are enforced automatically, for example in CI or a pre-commit hook, across the whole codebase, catching issues "before your code is executed." |

## Code documentation (15 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | There is no README and no comments; a new reader cannot tell what the project does or how to run it. |
| Initial | 3.75 | A minimal README exists but lacks setup or usage instructions, and the code has little to no explanatory comments. |
| Developing | 7.5 | A README covers purpose and basic usage, and non-trivial code sections have comments, but function- or API-level documentation is sparse for reusable code. |
| Strong | 11.25 | A README, inline comments, and docstrings or API documentation together let both users and future developers understand what the code does, why, and how to use or extend it. |
| Exemplary | 15 | Documentation is layered for its audience — a README for users, docstrings or API docs for developers, and comments for non-obvious logic — and is kept up to date with the code, reflecting that "programs must be written for people to read." |

## Licensing and open code (10 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | No license file is present and reuse terms are unstated, so others cannot legally use, modify, or redistribute the code. |
| Initial | 2.5 | A license is mentioned somewhere, such as in the README, but no `LICENSE` file is present, or the license's scope is unclear. |
| Developing | 5 | A `LICENSE` file is present in the project root, but code or bundled third-party components under a different license are not distinguished from it. |
| Strong | 7.5 | A clear, standard license file, recognizable by hosting platforms such as GitHub or GitLab, is present, and it is reasonably clear what license applies to which part of the project. |
| Exemplary | 10 | Licensing is explicit and unambiguous for every part of the project, including bundled third-party material, and the code is otherwise made openly accessible with enough documentation and metadata for others to discover, understand, and reuse it. |

## The Turing Way source map

- **Version control and collaborative review:** [Version Control](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/vcs.md) and [Code Review](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/reviewing.md).
- **Reproducible computational environments:** [Reproducible Environments](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/renv.md).
- **Testing:** [Testing](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/testing.md).
- **Continuous integration:** [Continuous Integration](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/ci.md).
- **Code quality: style and static analysis:** [Code Quality](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/code-quality.md).
- **Code documentation:** [Code Documentation](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/code-documentation.md) and [Code Reuse](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/code-reuse.md).
- **Licensing and open code:** [Licensing](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/licensing.md) and [Open Research](https://github.com/the-turing-way/the-turing-way/blob/7b7c9a5904a4c9382933b74409ca0705439baa27/book/website/reproducible-research/open.md).

These pages are public guidance from [The Turing Way](https://github.com/the-turing-way/the-turing-way),
a handbook to reproducible, ethical, and collaborative data science. The score
is this prototype's transparent mapping of that guidance, not an official The
Turing Way certification or institutional policy. No live retrieval tool is
available yet, so a review cites the repository, path, ref, and URL directly
from the pinned links above.
