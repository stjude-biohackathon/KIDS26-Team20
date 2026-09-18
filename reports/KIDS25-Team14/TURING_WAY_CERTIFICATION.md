# Turing Way-Aligned Readiness Snapshot

> **This is a Turing Way-aligned readiness snapshot, not an official
> certification.** The Turing Way is a set of public best-practice guidance
> for reproducible, ethical, and collaborative research — it is not a
> certification authority, and no institutional or funder body has
> authorized this document as a compliance certificate. Scores below reflect
> only what could be directly observed in the reviewed repository at the
> commit noted, using the ten-criterion rubric of the `turing-way-certified`
> skill.

- **Repository reviewed:** [`stjude-biohackathon/KIDS25-Team14`](https://github.com/stjude-biohackathon/KIDS25-Team14)
- **Commit reviewed:** `95c14e9075d231dd19c83a59624002aa9816f29a` (branch `main`)
- **Review date:** 2026-09-18
- **Scope:** Entire public repository as checked out at the commit above — README, LICENSE, `UI_main.R` Shiny app, `EnrichmentAnalysis/`, `notebooks/`, `data/`, `assets/`, `www/`, and git history/metadata. No private, restricted, or credentialed resources were accessed.
- **Confidence:** Medium-high. All ten repository facts below were directly observed in the checked-out working tree and cross-checked against the pinned commit before scoring; each was independently re-verified against the submitted repository URL to guard against evidence-tool cross-request mixing encountered during this review (see Limitations).

## Total score: 32 / 100

| # | Criterion | Score (0–10) |
|---|-----------|:---:|
| 1 | Project purpose and scope | 6 |
| 2 | Version control and provenance | 5 |
| 3 | Open collaboration | 3 |
| 4 | Reproducible environments | 2 |
| 5 | Data and workflow provenance | 4 |
| 6 | Testing and validation | 0 |
| 7 | Automation and continuous integration | 0 |
| 8 | Documentation and usability | 4 |
| 9 | Licensing, attribution, and responsible reuse | 5 |
| 10 | Ethics, accessibility, and sustainability | 3 |
| | **Total** | **32 / 100** |

## Criterion-by-criterion evidence

### 1. Project purpose and scope — 6/10
**Observation:** `README.md` states a clear biological research question
(mapping features shared by proteins with reduced solubility in aged mouse
tissue), the project's scope (enrichment analysis across GO/KEGG/structural
motifs), the intended solution (a Shiny app), and the team. It does not state
known limitations, a target skill level for users, or a minimum viable
product boundary.
[README.md at 95c14e9](https://github.com/stjude-biohackathon/KIDS25-Team14/blob/95c14e9075d231dd19c83a59624002aa9816f29a/README.md)

**Turing Way guidance:** [Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md) — recommends defining scope, goals, expected outcomes, resource requirements, and stakeholders before/alongside development.

### 2. Version control and provenance — 5/10
**Observation:** The repository has a real, incremental Git history (18+
commits) from multiple contributors, including merge commits that show
collaborative work. There are no Git tags or GitHub releases, so there is no
way to reference a stable, versioned snapshot of the software.
[Commit 95c14e9](https://github.com/stjude-biohackathon/KIDS25-Team14/commit/95c14e9075d231dd19c83a59624002aa9816f29a)

**Turing Way guidance:** [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md) — version control makes research transparent and traceable, and hosting services support structured collaboration (PRs, reviews, issues).

### 3. Open collaboration — 3/10
**Observation:** The README credits all five team members with GitHub
handles, showing basic attribution. There is no `CONTRIBUTING.md`,
`CODE_OF_CONDUCT.md`, or `.github/ISSUE_TEMPLATE` directory, so there is no
documented path, review expectation, or conduct standard for outside
contributors.
[Repository tree at 95c14e9](https://github.com/stjude-biohackathon/KIDS25-Team14/tree/95c14e9075d231dd19c83a59624002aa9816f29a)

**Turing Way guidance:** [Contributing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/contributing.md) — open, respectful dialogue and explicit contribution guidance/shared ownership standards support healthy collaboration.

### 4. Reproducible environments — 2/10
**Observation:** `UI_main.R` declares its dependencies only via `library()`
calls (`shiny`, `bslib`, `shinyjs`, `DT`, `readr`, `dplyr`, `tidyr`,
`ggplot2`, `ggrepel`, `ragg`, `tibble`). No `renv.lock`, `DESCRIPTION`,
`environment.yml`, or Dockerfile pins package versions or captures the R
environment, so re-creating the exact runtime is not possible from the repo
alone.
[UI_main.R at 95c14e9](https://github.com/stjude-biohackathon/KIDS25-Team14/blob/95c14e9075d231dd19c83a59624002aa9816f29a/UI_main.R)

**Turing Way guidance:** [Computational Reproducibility](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/pd-overview/pd-overview-repro.md) — recommends dependency managers and environment capture (e.g. containers) so others can recreate the setup process.

### 5. Data and workflow provenance — 4/10
**Observation:** `data/` contains over 20 versioned input/output files (e.g.
`folddisco_summary.csv`, `GSEA_results.csv`, `KEGG_Medicus_results.csv`) and
the `notebooks/` (`fetch_protein_data.ipynb`, `process_data_and_viz.ipynb`,
`Folddisco_Search.ipynb`, etc.) describe the processing steps in narrative
form. There is no data dictionary, schema, or `data/README.md` documenting
column meanings, units, or the provenance of each file.
[data/ at 95c14e9](https://github.com/stjude-biohackathon/KIDS25-Team14/tree/95c14e9075d231dd19c83a59624002aa9816f29a/data)

**Turing Way guidance:** [Research Data Management](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm.md) — recommends standardised file naming/folder structures, a data management plan, and documented data provenance.

### 6. Testing and validation — 0/10
**Observation:** No test files, test directories, or testing frameworks
(`testthat`, `pytest`, etc.) exist anywhere in the repository, and no
document describes how to validate the enrichment analysis or Shiny app
outputs.
[Repository tree at 95c14e9](https://github.com/stjude-biohackathon/KIDS25-Team14/tree/95c14e9075d231dd19c83a59624002aa9816f29a)

**Turing Way guidance:** [Testing Overview](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-overview.md) — automated and integration testing help expose faults early and build confidence in results.

### 7. Automation and continuous integration — 0/10
**Observation:** There is no `.github/workflows` directory or any other CI
configuration (e.g. Jenkins, GitLab CI, Travis) in the repository, so no
checks run automatically on new commits or pull requests.
[Repository tree at 95c14e9](https://github.com/stjude-biohackathon/KIDS25-Team14/tree/95c14e9075d231dd19c83a59624002aa9816f29a)

**Turing Way guidance:** [Continuous Integration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md) — CI integrates changes frequently and surfaces conflicts/bugs early, reducing manual testing burden.

### 8. Documentation and usability — 4/10
**Observation:** `README.md` (3,849 bytes) documents motivation, methods, and
the team, and `UI_main.R` has descriptive header comments. There is no
dedicated `docs/` folder, no step-by-step instructions for installing R
package dependencies, launching the Shiny app, or running the notebooks in
the correct order, and no stated limitations for end users.
[README.md at 95c14e9](https://github.com/stjude-biohackathon/KIDS25-Team14/blob/95c14e9075d231dd19c83a59624002aa9816f29a/README.md)

**Turing Way guidance:** [Project Documentation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md) — a good README should let readers understand what the project is about and how to use it.

### 9. Licensing, attribution, and responsible reuse — 5/10
**Observation:** The repository has a clear, unmodified MIT `LICENSE` file at
the root (Copyright St. Jude Children's Research Hospital BioHackathon,
2025), giving an identifiable, permissive reuse license. There is no
`CITATION.cff` file or other citation guidance telling reusers how to credit
the project.
[LICENSE at 95c14e9](https://github.com/stjude-biohackathon/KIDS25-Team14/blob/95c14e9075d231dd19c83a59624002aa9816f29a/LICENSE)

**Turing Way guidance:** [Licensing Checklist](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/licensing/licensing-checklist.md) — projects should select and clearly state a license, and citation guidance helps others credit the work correctly.

### 10. Ethics, accessibility, and sustainability — 3/10
**Observation:** All data files observed are non-human mouse
proteomics/enrichment results, which lowers immediate human-subjects/privacy
risk. The repository has no stated maintenance plan, archival strategy (e.g.
a Zenodo DOI or long-term hosting commitment), or accessibility statement for
the Shiny app or documentation.
[data/ at 95c14e9](https://github.com/stjude-biohackathon/KIDS25-Team14/tree/95c14e9075d231dd19c83a59624002aa9816f29a/data)

**Turing Way guidance:** [Ethics and Open-Source Governance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/ethical-research/ethics-open-source-governance.md) — sustainable, ethical open-source projects benefit from explicit governance, accessibility, and maintenance planning.

## Recommendations

1. **Add a limitations/scope note to the README** — state known limitations of the enrichment methods and target audience (Project Design guidance).
2. **Tag a release and adopt semantic versioning** — even a single `v0.1` tag would let others cite a stable snapshot (Version Control guidance).
3. **Add `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`** — clarify how external contributors can propose changes and what conduct is expected (Contributing guidance).
4. **Pin R dependencies with `renv::init()`/`renv.lock`** (or a Dockerfile) — capture exact package versions used by `UI_main.R` and the notebooks (Computational Reproducibility guidance).
5. **Document the `data/` directory** — add a short `data/README.md` describing each file's origin, columns, and how it was generated (Research Data Management guidance).
6. **Add minimal automated checks** — e.g. a `testthat` smoke test that the Shiny app's data-loading functions run without error (Testing guidance).
7. **Add a GitHub Actions workflow** — even a simple workflow that lints/`R CMD check`s on push would establish continuous integration (Continuous Integration guidance).
8. **Expand documentation with run instructions** — a "Getting Started" section listing required R packages and the order to run notebooks/launch the app (Project Documentation guidance).
9. **Add a `CITATION.cff` file** — make it easy for others to correctly cite the project alongside the existing MIT license (Licensing Checklist guidance).
10. **State a maintenance/archival plan** — note whether the repository will be archived (e.g. via Zenodo) after the hackathon concludes (Ethics and Open-Source Governance guidance).

## Limitations of this review

- This is a **readiness snapshot**, not a certification, audit, or guarantee of reproducibility, correctness, or security.
- Only observable, non-sensitive repository content at commit `95c14e9` was reviewed; no code was executed, and no external services (e.g. the AggrescanDB API referenced in the README) were tested.
- During evidence-tool queries, one batched (five-request) call to the Turing Way evidence tool returned citations and repository facts describing an unrelated repository, indicating a cross-request/cross-session data-mixing issue in the shared evidence backend during concurrent use. This review does not rely on that batched output: every one of the ten evidence packets used in the scores above was re-requested one at a time and individually verified to reference `stjude-biohackathon/KIDS25-Team14` before being used, and intermediate evidence files were relocated out of the shared `/tmp` directory into a uniquely named path inside this repository's working tree to avoid further cross-session file overwrites.
- Scores reflect the state of the repository at the reviewed commit only and will change as the project evolves.
