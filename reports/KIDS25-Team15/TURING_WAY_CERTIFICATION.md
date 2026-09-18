# Turing Way-Aligned Readiness Snapshot

> **This is not an official certification.** The Turing Way is a
> community-maintained handbook of best practices for reproducible,
> ethical, and collaborative research. This document is a transparent,
> evidence-based readiness snapshot scored against a ten-criterion rubric
> inspired by Turing Way guidance. It carries no legal, institutional, or
> official certifying authority, and a passing or high score does not
> constitute compliance with any funder, journal, or institutional policy.

- **Repository reviewed:** `stjude-biohackathon/KIDS25-Team15` ("Jude-E")
- **Review date:** 2026-09-18
- **Commit reviewed:** `c943fe51bae7e4f6457149200ebcaba0e8a29416` (branch `main`)
- **Scope:** Full public repository as checked out (frontend `judee-web/`,
  backend `backend/`, `notebooks/`, `docker-compose.yml`, root docs).
  Only accessible, non-sensitive repository documentation, configuration,
  and version-control history were inspected. No runtime execution,
  external service credentials, or private data were accessed.
- **Confidence:** Medium. Evidence is directly observed from the repository
  tree and Git history at the pinned commit above; the assessment
  reflects repository-visible practices only and cannot verify
  undocumented internal processes (e.g., informal code review conducted
  outside GitHub, or ethics discussions that took place off-repository).

## Method

1. Retrieved Turing Way guidance via the required evidence tools
   (`get_rag_status`, `get_turing_way_review_evidence`,
   `get_turing_way_evidence_packets`) before scoring.
2. Inspected the repository tree, README files, `LICENSE`, dependency
   manifests (`backend/requirements.txt`, `judee-web/package.json`),
   `docker-compose.yml`, `.gitignore`, and `git log`/`git tag` output at
   the pinned commit.
3. Scored each of the ten criteria below from 0 (no reliable evidence) to
   10 (clear, repeatable, and maintained practice), using only
   observations that could be directly verified in the repository.

## Ten-Criterion Score Table

| # | Criterion | Score (0–10) | Key Observed Evidence | Turing Way Guidance Cited |
|---|-----------|:---:|------------------------|----------------------------|
| 1 | Project purpose and scope | 6 | `README.md` clearly states Jude-E's purpose (an AI assistant helping patients navigate St. Jude facility/resources) and implied audience, but does not state scope boundaries, known limitations, or out-of-scope use. | [Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md) |
| 2 | Version control and provenance | 5 | `git log` shows ~40 commits with descriptive messages from 6 distinct authors (Aug–Oct 2025), but `git tag` returns no tags, there are no releases/CHANGELOG, and no branch-protection evidence is visible in the repo. | [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md) |
| 3 | Open collaboration | 1 | No `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/ISSUE_TEMPLATE`, or maintainership statement exists anywhere in the repository tree. | [Open Source Guide](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/open/open-source.md) |
| 4 | Reproducible environments | 5 | `backend/requirements.txt` pins some packages exactly (e.g. `grpcio==1.67.1`) but leaves others unpinned (`fastapi`, `chromadb`, `langchain`); `backend/Dockerfile` fixes a `python:3.11` base image. `judee-web/package.json` uses caret-ranged npm versions. No documented supported-version matrix or `.env.example` exists. | [Project Design – Methods](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/pd-overview/pd-overview-methods.md) |
| 5 | Data and workflow provenance | 1 | `backend/scrapped_data/` contains 7 CSV files (e.g. `scraped_output_metadata_new.csv`, `Events_SJ_patients.csv`) with no README, data dictionary, or provenance/source notes describing how or when they were collected. | [Research Data Management Checklist](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm/rdm-checklist.md) |
| 6 | Testing and validation | 0 | No test files, test directories, or documented validation/fixture instructions exist anywhere in the repository. | [Testing Guidance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-guidance.md) |
| 7 | Automation and continuous integration | 0 | There is no `.github/workflows` directory or any other CI configuration file in the repository. | [CI Practices](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci/ci-practices.md) |
| 8 | Documentation and usability | 5 | `README.md` gives step-by-step Ollama, npm, and docker-compose setup instructions; `judee-web/README.md` adds brief run commands. Neither includes usage examples, screenshots, troubleshooting guidance, or a stated limitations section. | [Code Documentation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md) |
| 9 | Licensing, attribution, and responsible reuse | 5 | Root `LICENSE` file contains the full MIT License text with a 2025 St. Jude Children's Research Hospital BioHackathon copyright notice, but there is no `CITATION.cff` or citation guidance, and no third-party attribution notes for scraped data or bundled assets. | [Open Source Guide](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/open/open-source.md); [Citable Software](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/communication/citable/citable-cite.md) |
| 10 | Ethics, accessibility, and sustainability | 0 | No file or README section addresses ethics/privacy review, patient data or PHI handling, accessibility, or a maintenance/archival plan, despite the project being a patient-facing assistant for a pediatric hospital. | [Stakeholder Personas](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/stakeholders/persona/persona-contributors.md) |
| | **Total** | **28 / 100** | | |

## Observed Repository Facts (with GitHub evidence links)

- README states project purpose: https://github.com/stjude-biohackathon/KIDS25-Team15/blob/c943fe51bae7e4f6457149200ebcaba0e8a29416/README.md
- Git history (6 authors, no tags): https://github.com/stjude-biohackathon/KIDS25-Team15/commits/c943fe51bae7e4f6457149200ebcaba0e8a29416
- No CONTRIBUTING/CODE_OF_CONDUCT/issue templates: https://github.com/stjude-biohackathon/KIDS25-Team15/tree/c943fe51bae7e4f6457149200ebcaba0e8a29416
- Backend dependency pinning: https://github.com/stjude-biohackathon/KIDS25-Team15/blob/c943fe51bae7e4f6457149200ebcaba0e8a29416/backend/requirements.txt
- Undocumented scraped CSV datasets: https://github.com/stjude-biohackathon/KIDS25-Team15/tree/c943fe51bae7e4f6457149200ebcaba0e8a29416/backend/scrapped_data
- No test/CI files: https://github.com/stjude-biohackathon/KIDS25-Team15/tree/c943fe51bae7e4f6457149200ebcaba0e8a29416
- README setup steps: https://github.com/stjude-biohackathon/KIDS25-Team15/blob/c943fe51bae7e4f6457149200ebcaba0e8a29416/README.md
- MIT LICENSE present, no citation file: https://github.com/stjude-biohackathon/KIDS25-Team15/blob/c943fe51bae7e4f6457149200ebcaba0e8a29416/LICENSE
- No ethics/accessibility/sustainability documentation: https://github.com/stjude-biohackathon/KIDS25-Team15/tree/c943fe51bae7e4f6457149200ebcaba0e8a29416

## Recommendations (prioritized)

1. **Add automated tests and CI** (criteria 6–7): introduce a minimal test
   suite (e.g. `pytest` for the FastAPI backend, a Vitest/Jest suite for
   `judee-web`) and a GitHub Actions workflow that runs them on every push
   and pull request.
2. **Document the scraped datasets** (criterion 5): add a `README.md` (or
   data dictionary) inside `backend/scrapped_data/` describing the source,
   collection date, scope, and schema of each CSV file.
3. **Add contribution and community-health files** (criterion 3): add
   `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`, and consider
   `.github/ISSUE_TEMPLATE` files.
4. **Address ethics, privacy, and sustainability** (criterion 10): since
   this is a patient-facing assistant for a pediatric hospital, document
   any ethical review, PHI/privacy handling safeguards, accessibility
   considerations, and a plan for ongoing maintenance or archival once the
   hackathon concludes.
5. **Add a `CITATION.cff`** (criterion 9) and pin all backend dependency
   versions in `requirements.txt` (criterion 4) for full reproducibility.
6. **Tag releases** and add a `CHANGELOG.md` (criterion 2) to improve
   provenance and traceability of shipped versions.

## Limitations

- This snapshot reflects only what is observable in the repository tree
  and Git metadata at the pinned commit; it cannot verify practices that
  exist outside the repository (e.g., private design discussions, informal
  ethics review, or manual QA not recorded in version control).
- Turing Way evidence was retrieved from a Retrieval-Augmented Generation
  (RAG) index over *The Turing Way* handbook (dataset `turing-way`,
  reported relevance score 89.0, 9 sources) and is cited to the pinned
  upstream commit `bb3f7abb56a40cd92a654fb51e4ec91f429cca2a` of
  `the-turing-way/the-turing-way`.
- No files other than this report and its PDF rendering were modified,
  installed, committed, or pushed as part of this review.

---

**Total score: 28 / 100** — This is a Turing Way-aligned readiness
snapshot, not an official Turing Way certification.
