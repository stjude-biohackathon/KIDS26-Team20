# Turing Way-Aligned Readiness Snapshot

> **This is not an official certification.** The Turing Way is a collection of
> open, community-authored best-practice guidance for reproducible,
> collaborative, and ethical research software. There is no Turing Way
> certifying body and no institutional or legal certification program behind
> this document. This report is a transparent, evidence-based readiness
> snapshot produced by comparing observable repository facts against
> Turing Way guidance. It should not be represented as compliance
> certification, a security audit, or an institutional approval.

- **Repository reviewed:** `stjude-biohackathon/KIDS25-Team7`
- **Commit reviewed:** `8ffebc71be4f49e97be206f9951bb02f417bdf65` (`origin/main`)
- **Review date:** 2026-09-18
- **Scope:** Entire public repository as checked out at the commit above (root
  files, `frontend/` application code, mock data, and configuration). No
  private branches, secrets, or non-public material were accessed.
- **Confidence:** **Medium.** Repository facts (file presence/absence,
  contents, and git history) were directly observed and are high-confidence.
  Turing Way guidance was retrieved via the project's RAG evidence tools with
  moderate-to-high relevance scores (~60–90%); criterion scores are a
  qualitative judgment applying that guidance to the observed facts, not a
  formula.

## Total Score

## **26 / 100**

This is a low readiness score, consistent with a small hackathon-origin
prototype (St. Jude BioHackathon, 2025) that has working application code but
has not yet adopted most reproducibility, collaboration, testing, or
governance practices described in The Turing Way.

## Score Table

| # | Criterion | Score (/10) | Repository Fact | Turing Way Guidance |
|---|-----------|:---:|------------------|----------------------|
| 1 | Project purpose and scope | 2 | Root `README.md` contains only the single line `# KIDS25-Team7`; no purpose, research question, intended users, or limitations are documented anywhere in the repository. | [Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md) |
| 2 | Version control and provenance | 6 | `git log` shows 59 commits across contributor branches (`adalecki`, `rschmitz2`, `esavage`, `frontend`) merged into `main` via numbered, reviewed pull requests (e.g. "Merge pull request #32"). No tags or releases exist, so there are no pinned, citable snapshots. | [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md) |
| 3 | Open collaboration | 3 | No `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, or `.github` issue/PR templates exist. A PR-review merge pattern is visible in git history, but no documented contribution path, review expectations, or maintainer/governance information exists. | [Collaboration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/collaboration.md) |
| 4 | Reproducible environments | 5 | `frontend/package-lock.json` (302 KB) pins exact dependency versions, and `frontend/README.md` documents `git clone` → `npm install` → `npm run start` setup steps. However, the root `package.json` is an empty `{}` object with no scripts/dependencies, and there is no containerization (e.g. Dockerfile) or documented Node/npm version requirement. | [Research Data Management Checklist](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm/rdm-checklist.md) |
| 5 | Data and workflow provenance | 1 | `frontend/public/db.json` (2071 bytes) and `routes.json` are committed as mock API data with no README, schema, or comments describing their fields, structure, or provenance. No workflow/pipeline documentation exists for how data flows through the app beyond code comments. | [Research Data Management Checklist](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm/rdm-checklist.md) |
| 6 | Testing and validation | 0 | A recursive search for `*.test.*` and `*spec*` across the repository (excluding `node_modules`) returned zero matches. No test framework is configured in `frontend/package.json`, and no validation/fixture files exist. | [Testing Guidance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-guidance.md) |
| 7 | Automation and continuous integration | 0 | No `.github` directory and no `*.yml`/`*.yaml` workflow files exist anywhere in the repository, so there is no CI running tests, linting, builds, or reproducibility checks on pushes or pull requests. | [Continuous Integration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md) |
| 8 | Documentation and usability | 4 | `frontend/README.md` (4581 bytes) documents application architecture, API flow, file organization, and a step-by-step development workflow with examples. The root `README.md` is a single 14-byte title line, there is no project-level `docs/` directory, and no end-user usage guide or documented limitations exist. | [Project Documentation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md) |
| 9 | Licensing, attribution, and responsible reuse | 5 | An MIT `LICENSE` file exists at the repository root, copyrighted to "St. Jude Children's Research Hospital BioHackathon (2025)", giving clear, permissive reuse terms. No `CITATION.cff` or citation guidance exists, and no third-party attribution notes are documented for bundled dependencies (e.g. Ketcher, RDKit). | [Licensing (FLOSS)](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/licensing/licensing-floss.md) |
| 10 | Ethics, accessibility, and sustainability | 0 | No file in the repository (README, LICENSE, or elsewhere) mentions data ethics/privacy handling, accessibility (e.g. WCAG) considerations, or a maintenance/archival plan for the project after the hackathon. | [Licensing and Ethical Source](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/licensing/licensing-ethical-source.md) |
| | **Total** | **26 / 100** | | |

## Checks Performed

- Read `README.md`, `LICENSE`, `package.json` at the repository root.
- Read `frontend/README.md`, `frontend/package.json`, `frontend/package-lock.json`,
  `frontend/eslint.config.js`, `frontend/.gitignore`.
- Listed `frontend/src` recursively (components, pages, api, types, utils, css).
- Searched the whole repository for `.github/` workflows, `*.yml`/`*.yaml`,
  `CONTRIBUTING*`, `CODE_OF_CONDUCT*`, `SECURITY*`, `CITATION*`, `*.test.*`,
  and `*spec*` files — all returned zero matches.
- Inspected `frontend/public/` (mock `db.json`, `routes.json`, logo assets).
- Reviewed `git log --oneline --all` (59 commits), `git branch -a` (4 remote
  contributor branches plus `main`), `git tag` (none), and
  `git shortlog -sn --all` (6 contributors).
- Retrieved Turing Way guidance via the required RAG evidence tools
  (`get_rag_status`, `get_turing_way_review_evidence`, `list_resources`,
  `query_mygpt_context`, `get_turing_way_evidence_packets`) before scoring.

## Recommendations

1. **Write a real root README** covering the project's purpose (a chemical
   compound registration/search tool built at the St. Jude BioHackathon),
   intended users, current scope, and known limitations. *(Criterion 1 —
   [Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md))*
2. **Tag a release** (e.g. `v0.1.0-hackathon`) to create a citable, pinned
   snapshot of the working prototype. *(Criterion 2 —
   [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md))*
3. **Add `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`** describing how to
   propose changes, review expectations, and community conduct standards.
   *(Criterion 3 —
   [Collaboration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/collaboration.md))*
4. **Populate the root `package.json` or add a top-level setup script**, and
   consider a Dockerfile or `.nvmrc`/engines field to capture the exact
   runtime environment. *(Criterion 4 —
   [RDM Checklist](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm/rdm-checklist.md))*
5. **Document `db.json`/`routes.json`** with a short schema description and
   note that they are mock/development data, not production data.
   *(Criterion 5 — same RDM Checklist reference)*
6. **Add automated tests** (e.g. Vitest/React Testing Library for the
   frontend) covering at least the API service layer and key components.
   *(Criterion 6 —
   [Testing Guidance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-guidance.md))*
7. **Add a GitHub Actions workflow** to run `npm run lint`, `npm run build`,
   and (once added) tests on every pull request. *(Criterion 7 —
   [Continuous Integration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md))*
8. **Expand documentation** beyond `frontend/README.md` with a top-level
   `docs/` overview linking to the frontend guide and describing overall
   project usage. *(Criterion 8 —
   [Project Documentation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md))*
9. **Add a `CITATION.cff`** so the software can be properly cited, and note
   licenses/attribution for bundled third-party components (Ketcher, RDKit).
   *(Criterion 9 —
   [Licensing (FLOSS)](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/licensing/licensing-floss.md))*
10. **State a data-handling/ethics note and a maintenance plan** — even a
    short statement on whether the app processes real research/patient data
    and who (if anyone) will maintain it after the hackathon. *(Criterion 10 —
    [Licensing and Ethical Source](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/licensing/licensing-ethical-source.md))*

## Limitations

- This snapshot reflects only the single commit reviewed
  (`8ffebc71be4f49e97be206f9951bb02f417bdf65`) and may not reflect
  subsequent changes.
- Only publicly observable repository content was reviewed; no CI logs,
  private discussions, issue trackers, or external documentation sites were
  inspected.
- Scores are qualitative judgments informed by Turing Way guidance, not a
  deterministic formula; a different reviewer applying the same rubric to
  the same evidence could reasonably assign adjacent scores (e.g. ±1–2
  points per criterion).
- This report is **not** an official Turing Way certification, security
  review, or institutional compliance approval. It is a best-practice
  readiness snapshot intended to help the team prioritize improvements.
