# Turing Way-Aligned Readiness Snapshot

> **This is a Turing Way-aligned readiness snapshot, not an official Turing
> Way certification.** The Turing Way is a set of public best-practice
> guidelines, not a certifying authority. No institution or program has
> endorsed this repository as "certified." Scores below reflect only what is
> directly observable in the reviewed repository at the reviewed commit.

- **Repository:** [stjude-biohackathon/KIDS25-Team4](https://github.com/stjude-biohackathon/KIDS25-Team4)
- **Reviewed ref:** `main` @ commit [`a8cec52`](https://github.com/stjude-biohackathon/KIDS25-Team4/commit/a8cec5270af8534953410c703d844cce5f50959a)
- **Review date:** 2026-09-18
- **Scope:** Full public repository tree (root files, `UI Files/`, `igv/`, `nf_integrated/`, `api_server.py`, `run.sh`, task/planning docs). No sensitive/private data reviewed.
- **Confidence:** Medium. Evidence is based on direct inspection of the file tree, README/task docs, LICENSE, environment files, git history/authors, and code entry points. Deep line-by-line review of every bundled third-party script (e.g. ANNOVAR Perl scripts, Java jars) was not performed.

## Score Summary

| # | Criterion | Score (0–10) |
|---|-----------|:---:|
| 1 | Project purpose and scope | 6 |
| 2 | Version control and provenance | 5 |
| 3 | Open collaboration | 2 |
| 4 | Reproducible environments | 4 |
| 5 | Data and workflow provenance | 3 |
| 6 | Testing and validation | 1 |
| 7 | Automation and continuous integration | 0 |
| 8 | Documentation and usability | 6 |
| 9 | Licensing, attribution, and responsible reuse | 5 |
| 10 | Ethics, accessibility, and sustainability | 1 |
| **Total** | | **33 / 100** |

## Criterion Detail

### 1. Project purpose and scope — 6/10
**Evidence:** `README.md` states the project goal ("Build and modernize the pipeline for usability and reproducibility"), names the two modules (WGS, MitoEdit), and includes a task list and a Mermaid workflow diagram.
**Gap:** No explicit statement of intended users, target audience, or known limitations/caveats of the pipeline.
**Repository fact:** README.md describes the WGS-MTE pipeline goal and module breakdown — https://github.com/stjude-biohackathon/KIDS25-Team4/blob/a8cec5270af8534953410c703d844cce5f50959a/README.md
**Turing Way guidance:** [Guide for Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md)

### 2. Version control and provenance — 5/10
**Evidence:** 30 commits on `main` with descriptive, categorized messages (e.g. "Update [shell]:", "New [YAML, shell]:") from multiple named contributors, tracked in a standard GitHub repo.
**Gap:** No tags or releases exist to mark reproducible snapshots; some commits bundle large third-party binary/annotation files together with pipeline changes, reducing change traceability.
**Repository fact:** git log shows 30 commits with descriptive messages, no tags found — https://github.com/stjude-biohackathon/KIDS25-Team4/commit/a8cec5270af8534953410c703d844cce5f50959a
**Turing Way guidance:** [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md)

### 3. Open collaboration — 2/10
**Evidence:** The repository is public and accepts GitHub's default issue/PR mechanisms; multiple named contributors appear in the git history.
**Gap:** No `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue templates, PR templates, or `.github/` directory exist. There is no documented review process or maintainer list.
**Repository fact:** No `.github` directory, CONTRIBUTING, or CODE_OF_CONDUCT files exist in the tree — https://github.com/stjude-biohackathon/KIDS25-Team4/tree/a8cec5270af8534953410c703d844cce5f50959a
**Turing Way guidance:** [Handling Technical Issues in a New Community](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/new-community/new-community-techissues.md)

### 4. Reproducible environments — 4/10
**Evidence:** Per-module Conda environment files exist (`igv/ends.yml`, `nf_integrated/nf_mte/mte.yml`, `nf_integrated/Mito_WGS_Nextflow/conda_environment/nf_mitvar.yml`, `annot_python2.yml`); README documents specific HPC module versions used (e.g. `samtools/1.12`, `bwa/0.7.17`).
**Gap:** No consolidated root-level environment/requirements file; no Docker/Singularity container yet (listed as an open TODO in README/TASKS.md); dependency pinning is inconsistent across the three separate `.yml` files.
**Repository fact:** Conda `.yml` files exist under `igv/` and `nf_integrated/` subfolders — https://github.com/stjude-biohackathon/KIDS25-Team4/blob/a8cec5270af8534953410c703d844cce5f50959a/nf_integrated/nf_mte/mte.yml
**Turing Way guidance:** [Open Source](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/open/open-source.md)

### 5. Data and workflow provenance — 3/10
**Evidence:** Nextflow (`Mitochondra_Variant_Call.nf`) and shell scripts encode workflow steps in code; a sample output fixture (`nf_integrated/nf_mte/test_WGS_output.tab`) exists.
**Gap:** No standalone data dictionary/schema documentation, no described data sources/provenance for reference/annotation files, and no explicit output-format documentation outside inline code/comments.
**Repository fact:** `nf_integrated/nf_mte/test_WGS_output.tab` is a sample output file without accompanying schema docs — https://github.com/stjude-biohackathon/KIDS25-Team4/blob/a8cec5270af8534953410c703d844cce5f50959a/nf_integrated/nf_mte/test_WGS_output.tab
**Turing Way guidance:** [Research Data Management Checklist](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm/rdm-checklist.md)

### 6. Testing and validation — 1/10
**Evidence:** README/TASKS.md list a "Validation" task (compare Nextflow outputs vs. legacy pipeline) as a planned, unchecked item.
**Gap:** No automated test suite, test runner, or CI-triggered checks exist. The only filename containing "test" (`test_WGS_output.tab`) is a static data fixture, not an executable test.
**Repository fact:** Repository tree contains only one file matching "test" (a data fixture), no pytest/unittest suite — https://github.com/stjude-biohackathon/KIDS25-Team4/tree/a8cec5270af8534953410c703d844cce5f50959a/nf_integrated/nf_mte
**Turing Way guidance:** [Testing Guidance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-guidance.md)

### 7. Automation and continuous integration — 0/10
**Evidence:** None found.
**Gap:** No `.github/workflows/` directory or any other CI configuration exists; no automated linting, testing, or packaging checks run on commits or pull requests.
**Repository fact:** No `.github/workflows` directory exists in the repository — https://github.com/stjude-biohackathon/KIDS25-Team4/tree/a8cec5270af8534953410c703d844cce5f50959a
**Turing Way guidance:** [Continuous Integration Practices](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci/ci-practices.md)

### 8. Documentation and usability — 6/10
**Evidence:** Root `README.md` is well-structured with goals, a checklist-style task list, a clarified outline, and a Mermaid workflow diagram; `api_server.py` opens with a module docstring describing its purpose; `igv/README.md` and `UI Files/readme.MD` provide module-level docs.
**Gap:** No unified setup/onboarding guide spanning all modules; several core capabilities (UI, containerization, validation) remain unchecked TODOs in the README itself, and code-level docstrings are sparse outside `api_server.py`.
**Repository fact:** `api_server.py` opens with a module docstring describing the API server purpose — https://github.com/stjude-biohackathon/KIDS25-Team4/blob/a8cec5270af8534953410c703d844cce5f50959a/api_server.py
**Turing Way guidance:** [Documenting your Project](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md)

### 9. Licensing, attribution, and responsible reuse — 5/10
**Evidence:** A permissive MIT `LICENSE` file exists at the repository root, correctly identifying the copyright holder (St. Jude Children's Research Hospital BioHackathon, 2025); the initial commit message credits the original Nextflow pipeline authors.
**Gap:** No `CITATION.cff` or structured citation file exists; the repository bundles third-party tools (ANNOVAR Perl scripts, `bambino-1.0.jar`, `picard.jar`, `mysql-connector-java`) without accompanying attribution/license files for those components.
**Repository fact:** `LICENSE` file at repo root grants MIT license to St. Jude Children's Research Hospital BioHackathon (2025) — https://github.com/stjude-biohackathon/KIDS25-Team4/blob/a8cec5270af8534953410c703d844cce5f50959a/LICENSE
**Turing Way guidance:** [Licensing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/LICENSE.md)

### 10. Ethics, accessibility, and sustainability — 1/10
**Evidence:** None found addressing ethics, data privacy, accessibility, or long-term maintenance/archival planning, despite the pipeline processing genomic sequencing data.
**Gap:** No ethics/data-governance statement, no accessibility considerations, and no stated maintenance or archival plan beyond an open task list.
**Repository fact:** No ETHICS, ACCESSIBILITY, or MAINTENANCE documentation files found in the repository tree — https://github.com/stjude-biohackathon/KIDS25-Team4/tree/a8cec5270af8534953410c703d844cce5f50959a
**Turing Way guidance:** [Accessibility](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/accessibility.md)

## Recommendations (priority order)

1. Add a `.github/workflows/` CI pipeline (lint + a smoke test) — highest-impact gap (Criteria 6 & 7 currently score 0–1).
2. Add `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` to enable structured open collaboration (Criterion 3).
3. Consolidate environment files into one pinned, documented environment (or the already-planned Docker/Singularity container) at the repo root (Criterion 4).
4. Add a `CITATION.cff` and attribution notes for bundled third-party tools (Criterion 9).
5. Add a short ETHICS/DATA-GOVERNANCE and maintenance/archival note given the genomic data domain (Criterion 10).
6. Document data schemas/provenance for pipeline inputs and outputs (Criterion 5).

## Limitations of this snapshot

- This is an automated, evidence-based snapshot generated with assistance from Turing Way RAG evidence retrieval; it is **not** a peer review, security audit, or institutional certification.
- Only the public repository tree at the pinned commit was inspected; private CI/organization-level policies (if any) outside this repo are not visible and were not scored.
- Scores are based on presence/absence of observable artifacts, not on runtime validation of the pipeline itself.

**Total score: 33 / 100**
