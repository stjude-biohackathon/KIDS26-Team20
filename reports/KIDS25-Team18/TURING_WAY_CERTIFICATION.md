# Turing Way-Aligned Readiness Snapshot

> **This is not an official certification.** The Turing Way is public
> best-practice guidance, not a certification authority or institutional
> policy. This document is a transparent, evidence-based readiness snapshot
> produced by inspecting observable repository artifacts, scored against a
> ten-criterion rubric (0–10 each, 100 points total). It carries no legal,
> regulatory, or institutional weight, and it does not evaluate scientific
> correctness, security, or ethical/legal compliance beyond what is visible
> in the repository.

- **Repository:** `stjude-biohackathon/KIDS25-Team18`
- **Reviewed commit:** `75406c545ec7a6c6cc6e390e2393834828deee08` (branch `main`, dated 2025-10-07)
- **Review date:** 2026-09-18
- **Scope:** Full public repository contents at the reviewed commit — source
  code (R, Python, Nextflow), documentation, licensing, and committed data
  artifacts. No private CI logs, issue/discussion history, or non-public
  metadata were available to inspect.
- **Confidence:** Moderate–High. Findings are based on direct inspection of
  the full working tree (all top-level files/directories), `git log`/`git tag`
  output, and file contents (README, LICENSE, `methynet/README`,
  `nextflow.config`, `main_nextflow.nf`). Confidence is not "High" because
  GitHub-hosted metadata not present in the local checkout (e.g., branch
  protection rules, Issues/Discussions activity, GitHub Actions run history
  beyond the absence of workflow files) could not be directly inspected.

## Score summary

| # | Criterion | Score (0–10) |
|---|-----------|:---:|
| 1 | Project purpose and scope | 0 |
| 2 | Version control and provenance | 4 |
| 3 | Open collaboration | 0 |
| 4 | Reproducible environments | 2 |
| 5 | Data and workflow provenance | 2 |
| 6 | Testing and validation | 0 |
| 7 | Automation and continuous integration | 0 |
| 8 | Documentation and usability | 2 |
| 9 | Licensing, attribution, and responsible reuse | 6 |
| 10 | Ethics, accessibility, and sustainability | 0 |
| **Total** | | **16 / 100** |

## Criterion detail

### 1. Project purpose and scope — 0/10
**Evidence:** `README.md` contains only the single line `# KIDS25-Team18`
(15 bytes total). No description of the research question, purpose, scope,
intended users, or known limitations exists anywhere in the repository.
**Check:** `cat README.md` → `# KIDS25-Team18`.
**Recommendation:** Add a README section stating the project's purpose
(e.g. the DepMap/methylation prediction goal implied by the code), intended
audience, and known limitations.
**Turing Way guidance:** [Subprojects](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/subprojects.md)

### 2. Version control and provenance — 4/10
**Evidence:** `git log` shows 46 commits on `main` with a GitHub remote
(`stjude-biohackathon/KIDS25-Team18`). Messages are mostly descriptive
(e.g. "Add test_genes", "KNN performance R plot") but some are informal
("post event", "accept ty's changes"). `git tag` returns no tags — there are
no versioned releases.
**Check:** `git log --oneline | wc -l` → 46; `git tag` → (empty).
**Recommendation:** Adopt tagged releases (e.g. semantic version tags) at
milestones, and use more consistently descriptive commit messages.
**Turing Way guidance:** [Contributors Record](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/contributors-record.md)

### 3. Open collaboration — 0/10
**Evidence:** No `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue/PR templates,
or `.github/` directory of any kind exist in the repository. No
maintainership information is documented.
**Check:** `find . -iname "CONTRIBUTING*" -o -iname "CODE_OF_CONDUCT*"` →
no results; `.github/` directory absent.
**Recommendation:** Add a `CONTRIBUTING.md` describing how to propose changes,
a `CODE_OF_CONDUCT.md`, and issue templates to set collaboration expectations.
**Turing Way guidance:** [Collaboration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/collaboration.md)

### 4. Reproducible environments — 2/10
**Evidence:** `methynet/README` documents manual `conda`/`pip` install steps
for one subcomponent (`conda create -n methylnet python=3.6`, `pip install
methylnet`), but no `requirements.txt`, `environment.yml`, `renv.lock`, or
Dockerfile exists anywhere in the repository for the R scripts
(`build_model*.R`), the Nextflow pipeline, or the `tabpfn_investigation`/`bin`
Python scripts.
**Check:** `find . -iname "*requirements*" -o -iname "*environment*.yml" -o
-iname "*renv*"` → no results outside the one narrative README.
**Recommendation:** Add pinned dependency manifests (e.g. `renv.lock` for R,
`environment.yml`/`requirements.txt` for Python) and, ideally, a container
definition for the Nextflow pipeline.
**Turing Way guidance:** [Data Usage Statement](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/data-usage-statement.md)

### 5. Data and workflow provenance — 2/10
**Evidence:** The repository root commits large data/result artifacts
directly (`depmap_predictions.csv` ~7.6 MB, `importance_df3_MYCN_XGB.csv`,
and four timestamped `results_*/` output directories) with no accompanying
documentation of their schema, generation date/parameters, or provenance. A
Nextflow workflow (`main_nextflow.nf`, `nextflow.config`,
`nextflow_modules/pfn_quick.nf`) does describe pipeline steps at a basic
level.
**Check:** `ls results_*` and `wc -l depmap_predictions.csv` (17,917 lines)
with no adjacent data dictionary.
**Recommendation:** Document each data file's origin, generation command,
and schema (e.g. a `DATA.md`), and consider excluding large generated
artifacts from version control in favor of a data-management plan.
**Turing Way guidance:** [Data Usage Statement](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/data-usage-statement.md)

### 6. Testing and validation — 0/10
**Evidence:** No test framework, test directory, or assertions exist. Files
named `test_genes.csv`, `small_test_input.txt`, and `large_test_jobs.txt` are
ad-hoc input data, not automated tests, and there is no documented procedure
for validating results.
**Check:** repository-wide search for test frameworks (pytest, testthat,
etc.) found none.
**Recommendation:** Add automated tests (e.g. `testthat` for R scripts,
`pytest` for Python) with representative fixtures and document how to run
them.
**Turing Way guidance:** [Glossary](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/glossary.md)

### 7. Automation and continuous integration — 0/10
**Evidence:** No `.github/workflows/` directory or any other CI
configuration (e.g. `.gitlab-ci.yml`, `Jenkinsfile`) exists in the
repository.
**Check:** `find .github/workflows` → not found.
**Recommendation:** Add CI (e.g. GitHub Actions) to run linting/tests on
pull requests and surface failures to contributors.
**Turing Way guidance:** [Legal Disclaimer](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/legal-disclaimer.md)

### 8. Documentation and usability — 2/10
**Evidence:** The top-level `README.md` is a one-line title with no usage
instructions. Only `methynet/README` documents setup/run instructions, and
only for that one subcomponent; the R model-building scripts, Nextflow
pipeline, and `tabpfn_investigation` scripts have no onboarding
documentation.
**Check:** `wc -c README.md` → 15 bytes; only one of several
subcomponents has any README.
**Recommendation:** Expand the top-level README with an overview, setup
instructions for each subcomponent, and usage examples.
**Turing Way guidance:** [Afterword](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/afterword.md)

### 9. Licensing, attribution, and responsible reuse — 6/10
**Evidence:** A clear MIT `LICENSE` file is present at the repository root,
attributed to "St. Jude Children's Research Hospital BioHackathon." No
`CITATION.cff` or explicit third-party attribution/reuse guidance exists for
bundled third-party tools referenced in the code (e.g. `methylnet`,
`pymethylprocess`, `tabpfn`).
**Check:** `cat LICENSE` confirms MIT terms; no `CITATION.cff` found.
**Recommendation:** Add a `CITATION.cff` for citing the repository and note
third-party tool licenses/attribution explicitly.
**Turing Way guidance:** [Legal Disclaimer](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/legal-disclaimer.md)

### 10. Ethics, accessibility, and sustainability — 0/10
**Evidence:** No files address data ethics/privacy (relevant given genomic
and cell-line data usage), accessibility of project outputs, or a
sustainability/maintenance/archival plan.
**Check:** Repository-wide search for ethics/privacy/accessibility/
maintenance documentation → none found.
**Recommendation:** Add a short statement on data governance/ethics for the
genomic data used, and a maintenance/archival plan (even informal, e.g. who
maintains this post-hackathon).
**Turing Way guidance:** [Data Usage Statement](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/data-usage-statement.md)

## Limitations of this snapshot

- This is a readiness snapshot based on static repository inspection at one
  commit, not an official Turing Way certification, security review, or
  scientific validation.
- GitHub-side collaboration signals (Issues, Discussions, PR review history,
  branch protection) were not accessible from the local checkout and were
  not scored as present or absent beyond what committed files show.
- Scores reflect only observable, verifiable evidence in the repository at
  the time of review; they may change as the repository evolves.

**Total score: 16 / 100**
