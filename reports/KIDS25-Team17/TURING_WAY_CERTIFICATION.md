# Turing Way-Aligned Readiness Snapshot

> **This is a Turing Way-aligned readiness snapshot, not an official
> certification.** The Turing Way is public best-practice guidance for
> reproducible, collaborative research, not a certifying body or
> institutional policy. This report does not constitute an authorized
> certification of any kind.

- **Repository:** `stjude-biohackathon/KIDS25-Team17`
- **Reviewed commit:** [`4ee8b5f`](https://github.com/stjude-biohackathon/KIDS25-Team17/tree/4ee8b5f15cfca38f59a0983bac8d86934fcc3c73) (`main`)
- **Review date:** 2026-09-18
- **Scope:** Full public repository contents at the reviewed commit — `README.md`, `LICENSE`, `app/app_v1/` (Streamlit app, conda environment export, GEO data/metadata files), `others/` (two Jupyter notebooks), `pics/`, and the Git history/commit metadata. No private data, credentials, or non-public information was inspected.
- **Overall confidence:** **Medium**. The repository is small and every file was read directly, but several judgments (e.g., extent of undocumented data provenance) rely on the absence of evidence rather than confirmed intent, and the retrieved Turing Way guidance passages, while on-topic, were retrieved via a general-purpose RAG index rather than hand-curated.

## Total score: **28 / 100**

## Score table

| # | Criterion | Score (0–10) | Key observed evidence |
|---|---|---|---|
| 1 | Project purpose and scope | 4 | README states the tool's purpose in three bullets with a schema diagram, but has no dedicated scope, intended-user, or limitations section. |
| 2 | Version control and provenance | 4 | Active multi-contributor Git history (10 authors, 30+ commits), but many messages are uninformative (`Update README.md`, `0.0.2`, `moving files`, `nav fix`) and there are no tags/releases. |
| 3 | Open collaboration | 2 | No `CONTRIBUTING`, `CODE_OF_CONDUCT`, or issue/PR templates; maintainer contact is informal (names/emails listed in the README "Acknowledgments" section only). |
| 4 | Reproducible environments | 4 | `app/app_v1/biohack25_clean.yml` pins hundreds of exact package versions, but it is a raw, machine-specific conda export (OS-specific builds, local channel URLs) rather than a curated cross-platform spec; setup instructions are four short README bullets with no supported-OS/Python-version guidance. |
| 5 | Data and workflow provenance | 3 | The GEO-scraping-to-Streamlit-app workflow exists in code (`others/*.ipynb` → `app/app_v1/*.csv`/`.txt` → `streamlite_app.py`), but there is no data dictionary, schema, or explanation of how the intermediate CSV/TXT/metadata files were produced or should be regenerated. |
| 6 | Testing and validation | 0 | No test files, test directory, or testing-framework configuration exist anywhere in the repository. |
| 7 | Automation and continuous integration | 0 | No `.github/workflows` directory or any other CI configuration exists. |
| 8 | Documentation and usability | 5 | README gives a clear project description, an embedded schema diagram, and a numbered "How to run it" section — enough for basic onboarding — but has no troubleshooting, limitations, or developer/API documentation for the 572-line `streamlite_app.py`. |
| 9 | Licensing, attribution, and responsible reuse | 5 | A standard MIT `LICENSE` is present (copyright St. Jude Children's Research Hospital BioHackathon, 2025) and contributors are credited by name/GitHub handle in the README, but there is no `CITATION.cff` or explicit reuse/citation guidance. |
| 10 | Ethics, accessibility, and sustainability | 1 | No file in the repository mentions accessibility, data-privacy/ethics considerations, or a maintenance/archival plan; the data is public GEO metadata so privacy risk appears low, but this is not documented. |
| | **Total** | **28 / 100** | |

## Evidence-backed recommendations

Each recommendation pairs a directly observed repository fact with a pinned Turing Way source retrieved for this review.

1. **Add automated tests and document how to run them.**
   - Observed: no test files, test directory, or testing-framework configuration exist anywhere in the repository at the pinned commit ([repo tree](https://github.com/stjude-biohackathon/KIDS25-Team17/tree/4ee8b5f15cfca38f59a0983bac8d86934fcc3c73)).
   - Guidance: [*Testing Guidance*](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-guidance.md) — "write some tests," run them regularly, and use a testing framework (e.g. `pytest`).

2. **Add continuous integration to run checks automatically.**
   - Observed: no `.github/workflows` directory or other CI configuration exists at the pinned commit ([repo tree](https://github.com/stjude-biohackathon/KIDS25-Team17/tree/4ee8b5f15cfca38f59a0983bac8d86934fcc3c73)).
   - Guidance: [*Testing Guidance*](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-guidance.md) — "consider setting up continuous integration ... to automatically run your tests each time you make a change."

3. **Adopt clearer, incremental commit messages and tagged releases.**
   - Observed: commit history contains many terse messages such as `Update README.md`, `0.0.2`, `moving files`, and `nav fix`, with no tags or releases ([commit history](https://github.com/stjude-biohackathon/KIDS25-Team17/commits/4ee8b5f15cfca38f59a0983bac8d86934fcc3c73)).
   - Guidance: [*General Workflow (Version Control)*](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs/vcs-workflow.md) — "clear and concise comments make it easier to get a fast overview of the changes ... your collaborators will thank you, but so will future versions of yourself."

4. **Add contribution guidance so external contributors know how to propose changes.**
   - Observed: no `CONTRIBUTING` file exists in the repository root or any subdirectory ([repo tree](https://github.com/stjude-biohackathon/KIDS25-Team17/tree/4ee8b5f15cfca38f59a0983bac8d86934fcc3c73)).
   - Guidance: [*Contributing*](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/contributing.md) — a contributing file describes how people can contribute and sets clear expectations for the process.

5. **Add a project scope/purpose statement covering intended users and limitations.**
   - Observed: the README states the tool's purpose (profiling GEO datasets) but does not describe intended users, limitations, or research scope ([README.md](https://github.com/stjude-biohackathon/KIDS25-Team17/blob/4ee8b5f15cfca38f59a0983bac8d86934fcc3c73/README.md)).
   - Guidance: [*Persona: Contributors*](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/stakeholders/persona/persona-contributors.md) — defining stakeholder personas helps a project clarify who it serves and which needs/limitations should be documented.

6. **Pin the conda environment to a curated, cross-platform, reproducible specification.**
   - Observed: `app/app_v1/biohack25_clean.yml` pins many packages with exact versions but is a machine-specific conda export including OS-specific build strings ([biohack25_clean.yml](https://github.com/stjude-biohackathon/KIDS25-Team17/blob/4ee8b5f15cfca38f59a0983bac8d86934fcc3c73/app/app_v1/biohack25_clean.yml)).
   - Guidance: [*General Workflow (Version Control)*](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs/vcs-workflow.md) — tracking versioned, well-documented environment/dependency files is part of good reproducible-research practice.

7. **Document accessibility considerations for the Streamlit app and its outputs.**
   - Observed: neither the README nor the app code contains an accessibility statement or considerations ([README.md](https://github.com/stjude-biohackathon/KIDS25-Team17/blob/4ee8b5f15cfca38f59a0983bac8d86934fcc3c73/README.md)).
   - Guidance: [*Accessibility*](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/accessibility.md) — accessibility practices help ensure project outputs and communications can be used by people with a wide range of needs.

## Checks performed

- Enumerated the full repository tree (`README.md`, `LICENSE`, `app/`, `others/`, `pics/`) at the pinned commit.
- Read `README.md` and `LICENSE` in full.
- Inspected `app/app_v1/biohack25_clean.yml` (conda environment export) and `app/app_v1/streamlite_app.py` (572 lines).
- Searched for `CONTRIBUTING`, `CODE_OF_CONDUCT`, `CITATION`/`.cff`, `.github/workflows`, and any file/directory matching `*test*` — none found.
- Reviewed `git log --all`, `git shortlog -sn --all`, and `git tag` output for provenance and release practices.
- Retrieved Turing Way guidance via the required evidence tools (`get_turing_way_review_evidence`, `list_resources`, `get_resource`, `get_turing_way_evidence_packets`) before scoring, covering project design, reproducibility, version control/collaboration, testing, contributing, accessibility, and persona/stakeholder guidance.

## Limitations

- This snapshot reflects only the single commit stated above; the repository may change afterward.
- Scoring reflects observable repository evidence only; internal team practices not captured in the repository (e.g., private communication norms) could not be assessed.
- The RAG evidence tool returned a fixed set of three combined-area passages plus targeted single-claim packets; broader Turing Way chapters were sampled via `list_resources`/`get_resource` rather than exhaustively reviewed.
- A score of 0 means no reliable evidence of the practice was found; 10 means the practice is clear, repeatable, and maintained. Intermediate scores reflect partial or inconsistent evidence as described per criterion above.
- This report is a readiness snapshot for continuous improvement, **not** an official Turing Way certification, endorsement, or compliance determination.
