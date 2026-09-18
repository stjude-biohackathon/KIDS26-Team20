# Turing Healthcheck Rubric

This rubric scores a codebase against eight practices from The Turing Way's
Reproducible Research guide, its Project Design guide, and its Community
Handbook / Guide for Collaboration, taken from chapters most directly
about how code is written, tested, shared, and collaborated on. 
Seven categories score code-facing practices; the eighth, added to reflect 
that The Turing Way is a handbook to "reproducible, ethical, and collaborative" 
data science, scores whether theproject identifies and manages its project 
team  and community.
The seven code-facing categories are weighted to sum to 60 points, and all
eight categories together sum to 65 raw points; when all eight are scored, the
earned raw total is converted to an overall percentage out of 100 by dividing
by 65 and multiplying by 100.

Select exactly one maturity level per category from observable repository
evidence. Follow [MCP source selection](#mcp-source-selection) below for the
required discovery, retrieval, and claim-level evidence workflow for every
selected category.
Do not average adjacent levels or silently reweight categories.
Category points are the category weight multiplied by the listed maturity
fraction; report category points to one decimal place and round the final
total to the nearest whole number.
For a requested-change review, apply each description only to the requested
change.
Use surrounding code as context and list pre-existing concerns without
deducting them from the change score.

## The Turing Way Project Design checklist

Before scoring, check the repository against this checklist from The Turing
Way's Project Design guide (Overview chapter). It is not a scored category by
itself; it is supporting evidence that informs several categories below —
mainly Version control and collaborative review, Licensing and open code, and
Community and stakeholder management. Note which items are present or absent
in the evidence you cite for those categories.

- **Before starting:** team and roles, funding and resources, the research
  question and scope, methodology, required approvals (for example ethics or
  data-access sign-off), and the license under which the work will be shared.
- **During the project:** version control practice and ongoing documentation
  of decisions and changes.
- **After completion:** archiving the project's outputs and code, and
  publishing or otherwise sharing the work with its intended audience.

MCP support: discover the Project Design Overview with
`learning-assistant_list_resources` and read it with
`learning-assistant_get_resource` before using this checklist. For each
checklist-based claim, call `learning-assistant_get_turing_way_evidence_packets`
with the Overview's returned `resource_id` and the applicable repository fact
under the skill's evidence rules. Each request selects one `resource_id` and
returns one citation. If a category also relies on another chapter, request a
separate evidence packet for that chapter's supporting claim and retain both
packets under the same category. Do not insert or replace citations in a
returned packet, or score the checklist separately.

## Version control and collaborative review (10 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | The code is not under version control, or its history does not show what changed, when, or by whom, and no review path exists for changes. |
| Initial | 2.5 | Code is under version control, but commit messages rarely explain why a change was made, unrelated changes are bundled together, and no pull or merge requests are used. |
| Developing | 5 | Commits are reasonably scoped and messaged on a hosted repository, but pull or merge requests and code review happen only occasionally, not as a habit. |
| Strong | 7.5 | Changes are captured as meaningful, well-messaged commits, and pull or merge requests are the norm, typically reviewed by at least one other contributor before merging. |
| Exemplary | 10 | History clearly documents what changed and why for every change, and every non-trivial change goes through recorded peer review before merging, in line with reviewing code as "an additional way of testing code quality." |

## Reproducible computational environments (10 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | Nothing in the repository identifies the runtime, language version, or dependencies, so another person cannot reconstruct the environment the code needs. |
| Initial | 2.5 | A dependency list exists (for example `requirements.txt` or `package.json`), but versions are unpinned or setup requires undocumented manual steps. |
| Developing | 5 | Dependencies are declared with pinned versions or a lockfile for the main workflow, but the environment itself is not captured in a portable, one-command form. |
| Strong | 7.5 | The environment is captured in a portable, versioned artifact (a lockfile plus documented setup, a Dockerfile, a conda environment file, or a Binder configuration) that a new contributor can use with minimal manual steps. |
| Exemplary | 10 | The full computational environment — dependencies, versions, and any needed services — is versioned, automated, and demonstrably reproducible from a clean machine, matching the guide's emphasis on "mobility of compute." |

## Testing (5 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | No automated tests exist; correctness depends on informal, undocumented manual checks. |
| Initial | 2 | Some ad hoc tests or scratch scripts exist, but they are not organized into a runnable test suite and are not repeatable. |
| Developing | 3 | Informal checks have been turned into functions collected in a test suite that covers the main happy path and can be run locally. |
| Strong | 4 | Tests cover both normal and failure or edge-case behavior, run repeatably, and act as a fail-fast safety net that catches regressions when code changes. |
| Exemplary | 5 | A maintained test suite covers critical behavior and edge cases, runs automatically, and gives clear, repeatable evidence that changes have not broken existing behavior. |

## Continuous integration (5 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | No CI is configured; any tests that exist are only ever run manually by individuals. |
| Initial | 2 | A CI configuration exists but is incomplete, is not actually triggered on commits or pull requests, or is frequently broken and ignored. |
| Developing | 3 | CI automatically runs the test suite on pushes or pull requests to the main branch, catching some regressions before merge. |
| Strong | 4 | CI runs on every commit or pull request, covers most of the test suite, and a failing run reliably blocks or flags problematic merges. |
| Exemplary | 5 | CI integrates changes frequently, runs the full test suite and related checks (such as linting) automatically, and a red CI run is treated as something to fix immediately, matching the guide's goal of finding bugs "early, minimizing their damage." |

## Code quality: style and static analysis (10 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | No consistent coding style is evident, and no linter or static analysis tool is configured or referenced anywhere in the project. |
| Initial | 2.5 | Some files follow a consistent style, but nothing enforces it, and inconsistency is common across the codebase. |
| Developing | 5 | A linter or static analysis tool (for example Pylint, ESLint, or shellcheck) is configured, but it is not run consistently and several flagged issues remain unresolved. |
| Strong | 7.5 | A linter or static analysis tool is configured and passes cleanly, or with justified exceptions, across most of the codebase, and style is consistent. |
| Exemplary | 10 | Static analysis and a consistent style are enforced automatically, for example in CI or a pre-commit hook, across the whole codebase, catching issues "before your code is executed." |

## Code documentation (10 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | There is no README and no comments; a new reader cannot tell what the project does or how to run it. |
| Initial | 2.5 | A minimal README exists but lacks setup or usage instructions, and the code has little to no explanatory comments. |
| Developing | 5 | A README covers purpose and basic usage, and non-trivial code sections have comments, but function- or API-level documentation is sparse for reusable code. |
| Strong | 7.5 | A README, inline comments, and docstrings or API documentation together let both users and future developers understand what the code does, why, and how to use or extend it. |
| Exemplary | 10 | Documentation is layered for its audience — a README for users, docstrings or API docs for developers, and comments for non-obvious logic — and is kept up to date with the code, reflecting that "programs must be written for people to read." |

## Licensing and open code (10 points)

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | No license file is present and reuse terms are unstated, so others cannot legally use, modify, or redistribute the code. |
| Initial | 2.5 | A license is mentioned somewhere, such as in the README, but no `LICENSE` file is present, or the license's scope is unclear. |
| Developing | 5 | A `LICENSE` file is present in the project root, but code or bundled third-party components under a different license are not distinguished from it. |
| Strong | 7.5 | A clear, standard license file, recognizable by hosting platforms such as GitHub or GitLab, is present, and it is reasonably clear what license applies to which part of the project. |
| Exemplary | 10 | Licensing is explicit and unambiguous for every part of the project, including bundled third-party material, and the code is otherwise made openly accessible with enough documentation and metadata for others to discover, understand, and reuse it. |

## Community and stakeholder management (5 points)

This category is not a Code of Conduct check. A Code of Conduct or
`CONTRIBUTING` file is one signal among several; the category mainly asks
whether the project has identified who its stakeholders are (maintainers,
contributors, users, funders, affected communities) and how they engage with
and communicate with the project, per the Project Design guide's Stakeholders
(Personas and Pathways) chapter and the Community Handbook's guidance on
communication channels and onboarding. Commit activity is scored as an
observable proxy for a living community: a project with no recent or ongoing
commit history has no active stakeholders to engage with, no matter how well
its governance documents read, so an inactive commit history caps the level
this category can reach even when documentation is otherwise strong. Check
recency (for example commits within roughly the last 3–6 months) and cadence
(more than a single burst of commits, from more than one contributor where
history allows) via `git log` before scoring.

| Level | Points | Observable description |
|---|---:|---|
| Missing | 0 | Nothing identifies who the project's stakeholders are (maintainers, contributors, users, or affected parties), there is no documented communication channel, there is no documented way for a newcomer to propose or make a change, and the commit history is stale or abandoned (no commits in a long time, or a single one-off dump with no ongoing activity). |
| Initial | 1 | Stakeholders or contributors are named informally (for example in a README credits section), but there is no stakeholder analysis, no defined communication channel (issue tracker use, mailing list, chat), and no `CONTRIBUTING` file or Code of Conduct; commit activity is sparse or irregular, with long gaps between commits. |
| Developing | 2.5 | Roles or stakeholder groups are documented (for example a `CONTRIBUTING` file describing maintainers vs. contributors, or a named communication channel such as issues or discussions), and a `CODE_OF_CONDUCT` file is present, but there is no explicit persona/pathway analysis or onboarding guidance for newcomers; commit history shows some recent, ongoing activity but is inconsistent. |
| Strong | 3.5 | Distinct stakeholder groups and their engagement pathways are documented (for example, separate guidance for users vs. contributors vs. maintainers, or a described decision-making/governance process), multiple communication channels are named and accessible, and the Code of Conduct and contributing guide are specific to the project; the commit history is active, with regular, recent commits. |
| Exemplary | 5 | Stakeholder and community management is explicit and actively maintained — documented personas or pathways for how different groups engage with the project, clearly signposted communication channels, onboarding (and, where relevant, offboarding) guidance, plus a specific Code of Conduct and contributing guide — matching the guide's view that "there is more to collaboration than we see" and that project design "is about people first." The commit history is active and sustained, with frequent, recent commits from more than one contributor where history allows, evidencing a genuinely engaged community rather than documentation alone. |

## MCP source selection

Use `learning-assistant_list_resources` to discover the current resource IDs,
following the pagination loop in step 3 of the [skill workflow](../SKILL.md#workflow),
then `learning-assistant_get_resource` to read the applicable sources before
scoring. Do not treat the first page as the full corpus. For every selected category, use
`learning-assistant_get_turing_way_evidence_packets` with one focused score
claim and one exact supporting `resource_id` per request. Include a
commit-pinned public GitHub repository fact when available; retain local
evidence separately under the skill's evidence rules otherwise. A category
may need multiple packets, but receives only one maturity level and score.
Send one to five requests per call, batching by request count.

Cite only each packet's returned Turing Way citation and matching RAG
relevance score. Do not manually construct a source URL, resource ID, or
relevance score. Choose only from the following chapter topics; the MCP
output, not this list, supplies the final title, repository, path, ref, URL,
and relevance score.

| Category | Turing Way chapter topics to retrieve |
|---|---|
| Version control and collaborative review | Version Control; Code Review |
| Reproducible computational environments | Reproducible Environments |
| Testing | Testing |
| Continuous integration | Continuous Integration |
| Code quality: style and static analysis | Code Quality |
| Code documentation | Code Documentation; Code Reuse |
| Licensing and open code | Licensing; Open Research |
| Community and stakeholder management | Project Design Overview; Stakeholders: Personas and Pathways; Code of Conduct; Contributing; Guide for Collaboration |

These chapters are public guidance from The Turing Way, a handbook to
reproducible, ethical, and collaborative data science. The score is a
transparent mapping of that guidance, not an official Turing Way certification
or institutional policy.
