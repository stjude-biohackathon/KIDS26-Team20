# Turing Way-Aligned Readiness Snapshot

**This is a Turing Way-aligned readiness snapshot produced with the assistance of
public [The Turing Way](https://github.com/the-turing-way/the-turing-way) guidance.
It is NOT an official Turing Way certification.** The Turing Way project does not
operate a certification authority, and no such authority was consulted. Scores
reflect only what could be directly observed in the reviewed repository at the
commit noted below.

- **Repository reviewed:** [`stjude-biohackathon/KIDS25-Team5`](https://github.com/stjude-biohackathon/KIDS25-Team5)
- **Commit reviewed:** `d614403d24f8d1842c7aaae698932654a2aedba8`
- **Review date:** 2026-09-18
- **Scope:** Entire public repository as checked out (data dictionaries, SAS/CSV
  datasets, metadata guides, `README.md`, `LICENSE`, `WORKFLOW.md`). No private,
  restricted, or credential-bearing files were reviewed.
- **Confidence:** Medium. The repository is a data-and-documentation project
  (no application source code), so several rubric criteria written for software
  projects had limited applicable evidence to find; absence of evidence for a
  practice was scored as such, not assumed to be a hidden strength.

## Ten-Criterion Score Table

Each criterion is scored 0–10 (0 = no reliable evidence found, 5 = partially or
inconsistently documented, 10 = clear, repeatable, and maintained). The total
is out of 100.

| # | Criterion | Score (/10) | Key Observed Evidence |
|---|-----------|:-----------:|------------------------|
| 1 | Project purpose and scope | 3 | [`README.md`](https://github.com/stjude-biohackathon/KIDS25-Team5/blob/d614403d24f8d1842c7aaae698932654a2aedba8/README.md) is a single line (`# KIDS25-Team5`); scope, research question, and limitations are only inferable from [`metadata/AI_navigation_guide.md`](https://github.com/stjude-biohackathon/KIDS25-Team5/blob/d614403d24f8d1842c7aaae698932654a2aedba8/metadata/AI_navigation_guide.md), not stated up front. |
| 2 | Version control and provenance | 4 | 24 commits from 4 authors give some history, but ~1.5GB of `.sas7bdat` files and ~672MB of CSVs are committed directly to Git with no `.gitattributes`/Git LFS, and there are no tags or releases. |
| 3 | Open collaboration | 3 | 5 open GitHub issues show active task tracking, but there is no `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, or `.github/` community-health directory anywhere in the repository. |
| 4 | Reproducible environments | 1 | No `requirements.txt`, `environment.yml`, `Dockerfile`, notebooks, or analysis code exist; the repository holds only data and two Markdown documents. |
| 5 | Data and workflow provenance | 6 | `metadata/AI_navigation_guide.md`, `metadata/cohort_timeline_map.md`, `metadata/directory_structure_guide.md`, `metadata/questionnaire_cross_reference.md`, `dictionary/readme.txt`, and folder-level READMEs (e.g. `sasdata/obase23/README.md`) document structure and variables well, but no formal data management plan or explicit versioning/naming policy is stated. |
| 6 | Testing and validation | 0 | No test files, test directories, or documented validation/data-quality checks were found anywhere in the repository. |
| 7 | Automation and continuous integration | 0 | No `.github/workflows` directory or other CI configuration exists. |
| 8 | Documentation and usability | 5 | [`WORKFLOW.md`](https://github.com/stjude-biohackathon/KIDS25-Team5/blob/d614403d24f8d1842c7aaae698932654a2aedba8/WORKFLOW.md) documents a proposed application workflow with a Mermaid diagram, and the `metadata/`/`dictionary/` guides are detailed, but the root `README.md` does not link to any of them, and there is no roadmap or changelog. |
| 9 | Licensing, attribution, and responsible reuse | 4 | An MIT [`LICENSE`](https://github.com/stjude-biohackathon/KIDS25-Team5/blob/d614403d24f8d1842c7aaae698932654a2aedba8/LICENSE) is present at the root, but there is no `CITATION.cff` or other citation/attribution guidance for reusing the dataset. |
| 10 | Ethics, accessibility, and sustainability | 1 | The repository holds pediatric cancer survivor cohort (CCSS) survey data; only a single named contact e-mail appears in `dictionary/readme.txt`/`metadata/readme.txt`, with no visible ethics/IRB/consent/data-sharing statement and no accessibility or archival/sustainability plan. |
| **Total** | | **27 / 100** | |

## Recommendations (with Turing Way Citations)

1. **Expand `README.md`** to state the project's research question/purpose,
   intended users, scope, and known limitations, per The Turing Way's
   [Guide for Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md).
   *Repository fact:* [`README.md`](https://github.com/stjude-biohackathon/KIDS25-Team5/blob/d614403d24f8d1842c7aaae698932654a2aedba8/README.md) is currently a single line.
2. **Adopt Git LFS (or an equivalent) for large binary datasets** to keep
   provenance traceable without bloating the main Git history, per The Turing
   Way's [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md) chapter.
   *Repository fact:* ~1.5GB of `.sas7bdat` files under [`sasdata/`](https://github.com/stjude-biohackathon/KIDS25-Team5/tree/d614403d24f8d1842c7aaae698932654a2aedba8/sasdata) are committed directly with no LFS configuration.
3. **Add `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`** to formalize how outside
   contributors can engage, per The Turing Way's
   [Contributing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/contributing.md) guidance.
   *Repository fact:* No `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, or `.github/` directory exists; 5 open issues track work informally.
4. **Document or provide a reproducible computational environment** (e.g. a
   `requirements.txt`/`environment.yml` and analysis scripts/notebooks) so
   others can recreate any processing of this data, per The Turing Way's
   [Reproducibility Methods](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/pd-overview/pd-overview-methods.md).
   *Repository fact:* the repository root has no dependency manifest, container definition, or code/notebooks.
5. **Write a Data Management Plan / naming and versioning policy** to
   complement the existing dictionaries and guides, per The Turing Way's
   [Research Data Management Checklist](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm/rdm-checklist.md).
   *Repository fact:* `metadata/` and `dictionary/` document structure and variables well but no DMP exists.
6. **Add automated or documented validation checks** for the datasets (e.g.
   schema/row-count checks), per The Turing Way's
   [Code Testing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing.md) chapter.
   *Repository fact:* no test files or validation scripts exist in the repository.
7. **Introduce CI automation** (e.g. GitHub Actions) once code or checks
   exist, so that failures are visible to contributors, per The Turing Way's
   [Continuous Integration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md) chapter.
   *Repository fact:* no `.github/workflows` or other CI configuration exists.
8. **Link the root README to `WORKFLOW.md` and the `metadata/`/`dictionary/`
   guides**, and add a roadmap/changelog, per The Turing Way's
   [Project Documentation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md) guidance.
   *Repository fact:* `WORKFLOW.md` and the metadata guides exist but are not referenced from `README.md`.
9. **Add a `CITATION.cff`** describing how to cite this dataset/repository, in
   addition to the existing MIT `LICENSE`, per The Turing Way's
   [Licensing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/licensing.md) chapter.
   *Repository fact:* [`LICENSE`](https://github.com/stjude-biohackathon/KIDS25-Team5/blob/d614403d24f8d1842c7aaae698932654a2aedba8/LICENSE) (MIT) exists but no `CITATION.cff` does.
10. **Document ethics/consent/data-sharing status and an accessibility or
    sustainability/archival plan**, given this repository holds pediatric
    cancer survivor cohort survey data, per The Turing Way's
    [Accessibility](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/accessibility.md) chapter.
    *Repository fact:* `dictionary/readme.txt`/`metadata/readme.txt` provide only a contact e-mail, with no ethics/IRB/consent statement or accessibility/sustainability plan found.

## Limitations of This Review

- This snapshot is not an official Turing Way certification; The Turing Way
  publishes best-practice guidance, not a certifying body or standard.
- The review is based on static inspection of the repository at one commit
  and did not execute any code, since none exists in the repository.
- Sensitive material (credentials, PHI, restricted files) was excluded from
  consideration; the absence of an ethics/consent statement is reported as an
  observed documentation gap, not a determination about the underlying data
  governance, which may exist outside this repository.
- Scores reflect only what is directly observable in this repository; any
  undocumented practices that exist elsewhere (e.g., institutional IRB
  approvals, private CI, or internal contribution processes) were not
  visible to this review and could not be credited.

## Total Score: 27 / 100
