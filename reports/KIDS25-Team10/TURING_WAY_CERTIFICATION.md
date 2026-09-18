# Turing Way-Aligned Certification Readiness Review

**Repository:** [stjude-biohackathon/KIDS25-Team10](https://github.com/stjude-biohackathon/KIDS25-Team10)
**Reviewed ref:** `d7d962b64312d81c76ed0003b155a237a22fcf72` (public `main` snapshot)
**Review date:** 2026-09-18
**Scope:** Public repository documentation, source layout (R/RMarkdown scripts), licensing, and Git/automation metadata. No file contents were modified, and no patient identifiers, data files, or credentials were opened or reproduced.
**Confidence:** Moderate. The full public repository tree (8 tracked files) was inspected directly via the commit-pinned Git tree and GitHub API metadata. The R/RMarkdown scripts were not executed: they require R packages that are not installed in this session and reference local, non-portable file paths.

> This is a transparent Turing Way-aligned readiness snapshot, not an official Turing Way certification, institutional approval, privacy assessment, clinical validation, or security audit.

## Result

**Overall readiness score: 25 / 100 - Initial/Developing readiness**

The repository documents a clear hackathon goal (data "finder"/crawler tools for the Department of Psychology and Biobehavioral Science) with reasonably descriptive READMEs and an MIT license. Readiness is limited by an essentially unmanaged version history (two commits, no tags), no contribution or review process, unpinned R dependencies with no captured environment, no automated tests or CI, and — notably for tools that search files by patient MRN — no documented privacy/ethics, accessibility, or maintenance/archival practices.

## Ten-criterion score table

| # | Criterion | Score (0-10) | Evidence observed | Priority improvement |
|---:|---|---:|---|---|
| 1 | Project purpose and scope | 5 | Root `README.md` names the project ("Project FINDIT"), its sponsoring department, the "finder"/crawler concept, prior-year history, and this year's focus. It does not state intended users beyond "researchers," known limitations, or a definition of success. | Add explicit scope, supported use cases, limitations, and success criteria to the root README. |
| 2 | Version control and provenance | 2 | Public Git history exists but contains only two commits ("Initial commit", "uploading files"), no tags, no releases, and no changelog. | Adopt incremental commits with descriptive messages, and tag releases for reproducible provenance. |
| 3 | Open collaboration | 1 | A README and MIT license exist. No `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue/PR templates, or documented review process were found anywhere in the tree. | Add contribution, review, and code-of-conduct guidance so external collaborators know how to participate. |
| 4 | Reproducible environments | 1 | Both sub-project READMEs list R packages to install via `install.packages(...)` with no version pins, and no `renv.lock`, `DESCRIPTION`, Dockerfile, or Binder configuration exists anywhere in the repository. | Pin R package versions (e.g., with `renv`) and document the supported R version. |
| 5 | Data and workflow provenance | 3 | READMEs describe crawler inputs/outputs in some detail (e.g., "Saves results to `../data/processed_data/file_inventory_updated.csv`", supported file types), but no data dictionary, source/schema documentation, or refresh process for the underlying MRN-indexed data is present. | Document the schema, provenance, and refresh/rebuild steps for the crawled data and generated inventories. |
| 6 | Testing and validation | 0 | The only test-like file, `Archive/test_ggtree.R`, is a 15-line ad hoc script that hardcodes a local user's home-directory path (`/Users/kgibney/Documents/fNIRS_Data`) and is unrelated to, and not runnable against, the two main crawler tools. No automated test suite exists. | Add deterministic, portable tests (e.g., fixture directories) for the file-crawler and participant-finder logic. |
| 7 | Automation and continuous integration | 0 | No `.github/workflows` directory or any other CI configuration is present in the commit-pinned recursive tree. | Add CI to lint/build the R scripts and run any new automated tests on every push/PR. |
| 8 | Documentation and usability | 6 | The root and two sub-project READMEs clearly describe purpose, features, required R packages, and output locations, giving a reasonable onboarding path for R users. They lack architecture, troubleshooting, or developer-workflow documentation. | Expand docs with setup verification steps, troubleshooting, and a short architecture/data-flow overview. |
| 9 | Licensing, attribution, and responsible reuse | 6 | A standard MIT `LICENSE` file is present at the repository root. No `CITATION.cff` or attribution guidance for third-party packages/data exists. | Add a `CITATION.cff` and document attribution/reuse terms for any third-party data or code. |
| 10 | Ethics, accessibility, and sustainability | 1 | The tools are explicitly designed to "search files for a specific MRN" and report available data per patient, but the repository has no privacy/ethics statement, data-handling/retention policy, accessibility considerations, or maintenance/archival plan. | Document privacy/ethics boundaries for MRN-based searches, and add an ownership/maintenance and archival plan. |
| **Total** |  | **25 / 100** |  |  |

## Evidence and checks

- Public repository metadata: MIT-licensed, non-archived, `main` default branch, 1 open issue, 2 contributors, most recently pushed 2025-09-30 ([repository metadata](https://api.github.com/repos/stjude-biohackathon/KIDS25-Team10)).
- The complete commit-pinned recursive tree contains exactly 8 files: `README.md`, `LICENSE`, `Archive/test_ggtree.R`, `File Crawler/README.md`, `File Crawler/file_crawler.Rmd`, `Participant First Finder/README.md`, `Participant First Finder/participant_first_findr.Rmd` — no test directory, environment manifest, CI workflow, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, or `CITATION.cff` ([commit-pinned recursive tree](https://api.github.com/repos/stjude-biohackathon/KIDS25-Team10/git/trees/d7d962b64312d81c76ed0003b155a237a22fcf72?recursive=1)).
- `README.md` describes Project FINDIT's goals, prior-year and current-year hackathon scope, and the two "finder" tools ([commit-pinned README](https://github.com/stjude-biohackathon/KIDS25-Team10/blob/d7d962b64312d81c76ed0003b155a237a22fcf72/README.md)).
- `File Crawler/README.md` and `File Crawler/file_crawler.Rmd` describe an R script that recursively inventories files and extracts unique MRN counts from `.sas7bdat` files, listing unpinned `install.packages()` dependencies ([commit-pinned File Crawler README](https://github.com/stjude-biohackathon/KIDS25-Team10/blob/d7d962b64312d81c76ed0003b155a237a22fcf72/File%20Crawler/README.md)).
- `Participant First Finder/README.md` and `.../participant_first_findr.Rmd` describe a workflow that searches CSV/Excel/SAS files for a specific patient MRN across a directory tree, again with unpinned dependencies ([commit-pinned Participant First Finder README](https://github.com/stjude-biohackathon/KIDS25-Team10/blob/d7d962b64312d81c76ed0003b155a237a22fcf72/Participant%20First%20Finder/README.md)).
- `LICENSE` contains the standard MIT license text ([commit-pinned LICENSE](https://github.com/stjude-biohackathon/KIDS25-Team10/blob/d7d962b64312d81c76ed0003b155a237a22fcf72/LICENSE)).
- `Archive/test_ggtree.R` is a 15-line scratch script using `ggtree`/`fs::dir_tree` against a hardcoded local path; it is not a portable or automated test ([commit-pinned test_ggtree.R](https://github.com/stjude-biohackathon/KIDS25-Team10/blob/d7d962b64312d81c76ed0003b155a237a22fcf72/Archive/test_ggtree.R)).
- Commit history at the reviewed ref contains only two commits with no tags or releases ([commit history](https://github.com/stjude-biohackathon/KIDS25-Team10/commits/d7d962b64312d81c76ed0003b155a237a22fcf72)).
- No script execution was attempted: the R scripts require packages (`tidyverse`, `haven`, `data.table`, `ggtree`, etc.) not installed in this session, and `Archive/test_ggtree.R` hardcodes a path (`/Users/kgibney/Documents/fNIRS_Data`) that does not exist in this environment.

## Prioritized recommendations

1. **Add deterministic, portable tests and CI** for the file-crawler and participant-finder R scripts, using small non-sensitive fixture directories, and run them automatically on every push/PR.
2. **Pin R dependencies and capture the environment** (e.g., an `renv.lock` or `DESCRIPTION` file) instead of unversioned `install.packages()` calls.
3. **Add contributor and governance documentation** — `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and issue/PR templates — to support open, reviewable collaboration.
4. **Document privacy/ethics handling for MRN-based searches** and add an explicit maintenance/archival owner, since the tools are designed to locate patient-identifiable data across a filesystem.
5. **Add a `CITATION.cff`** and document the data schema/provenance for the file inventories the tools produce.

## Pinned Turing Way guidance

- [Guide for Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md) — define scope, goals, users, constraints, and success measures.
- [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md) — track provenance through meaningful commit and release history.
- [Guide for Collaboration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/collaboration.md) — support inclusive contribution, review, and expectations.
- [Reproducible Environments](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/renv.md) — capture and pin computational environments.
- [Guide for Reproducible Research](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/reproducible-research.md) — make data, code, and workflows available for rerunning analyses.
- [Code Testing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing.md) — write and maintain automated tests.
- [Continuous Integration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md) — automate tests and checks on every change.
- [Code Quality](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-quality.md) — apply linting and static analysis.
- [The Turing Way License](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/LICENSE.md) — pinned source used for licensing and responsible-reuse context.
- [Accessibility Policy](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/accessibility/accessibility-policy.md) — used for accessibility, ethics, and sustainability context.

## Limitations

This review scores observable repository evidence only. It does not certify the software, execute the R scripts, verify runtime behavior, inspect any patient data, evaluate clinical or research validity, perform a security audit, or establish institutional/legal compliance (e.g., HIPAA). Missing documentation was scored as missing evidence rather than inferred practice. The score may change when the repository changes or when maintainers provide verifiable artifacts.
