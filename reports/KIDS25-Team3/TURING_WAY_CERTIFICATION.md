# Turing Way-Aligned Readiness Snapshot

> **This is a Turing Way-aligned readiness review, not an official certification.**
> _The Turing Way_ is public best-practice guidance produced by a community project; it is not a
> certification authority, accreditation body, or institutional policy. No score below implies
> endorsement, compliance sign-off, or legal/regulatory approval. Treat this as a transparent,
> point-in-time snapshot of observable repository practices measured against Turing Way guidance.

- **Review date:** 2026-09-18
- **Repository reviewed:** `stjude-biohackathon/KIDS25-Team3`
- **Reviewed commit:** `da0c26763f5d6097e78fea1ec1bb992afedc364d` (branch `main`)
- **Scope:** Public repository root and all tracked files (README, LICENSE, `gui.py`, `data/`,
  `presentation/`, `resources/`, `scripts/`, `src/`, `videos/`, `yolo_labels/`, and Git history).
  No non-public, credentialed, or PHI-restricted material was accessed.
- **Confidence:** **Medium.** The full working tree and Git history were directly inspected, but
  no CI logs, issue tracker activity, or external documentation (e.g. a project wiki) exist to
  corroborate practices beyond what is committed to the repository.

## Ten-criterion rubric (0–10 each, integer scores, total out of 100)

| # | Criterion | Score | Observed evidence |
|---|-----------|:-----:|--------------------|
| 1 | Project purpose and scope | 3 | `README.md` is a single-line title plus a 6-step script pipeline with no scope, intended-user, or limitations statement; a project-rationale paragraph ("Why Our Project Matters") exists only inside a GUI label string in `gui.py`, not as standalone documentation. |
| 2 | Version control and provenance | 6 | 52 commits from 6+ contributors with descriptive merge commits referencing pull requests (e.g. "Merge pull request #10 from stjude-biohackathon/feature/GUI"), but `git tag` returns no tags/releases marking citable snapshots. |
| 3 | Open collaboration | 2 | No `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue templates, or `.github/` directory exist anywhere in the tree, despite multiple contributors and PR-based merges visible in history. |
| 4 | Reproducible environments | 3 | `requirements.txt` pins 18 dependencies (e.g. `opencv-python==4.12.0.88`, `ultralytics==8.3.204`), but the file is encoded as UTF-16LE with CRLF line endings, which breaks a standard `pip install -r requirements.txt`; no README setup instructions, Dockerfile, or environment capture exist. |
| 5 | Data and workflow provenance | 2 | `data/yaml.yaml` defines only bare YOLO dataset fields (`path`, `train/val/test`, one class `rs_board`); scripts (`src/train.py`, `src/test.py`) use hardcoded relative paths with no data dictionary, source description, or provenance notes. |
| 6 | Testing and validation | 1 | No automated test suite exists; the only file named `test.py` (`src/test.py`) is a manual YOLO inference script with no assertions, fixtures, or `pytest`/`unittest` usage. |
| 7 | Automation and continuous integration | 0 | No `.github/workflows` directory or any CI configuration exists; the repository's only YAML file (`data/yaml.yaml`) is a dataset config, not automation. |
| 8 | Documentation and usability | 2 | `README.md` (708 bytes) lists only manual data-prep steps and a filename convention; it never mentions `gui.py` (a 21KB PyQt5 application), the `scripts/` tools, or how to install/run any part of the project. |
| 9 | Licensing, attribution, and responsible reuse | 5 | A complete MIT `LICENSE` file is present with a clear institutional copyright holder ("St. Jude Children's Research Hospital BioHackathon"), but there is no `CITATION.cff`, no citation guidance, and no attribution for third-party dependencies (e.g. Ultralytics YOLO, PyQt5) or bundled media assets. |
| 10 | Ethics, accessibility, and sustainability | 1 | Despite processing proton beam radiotherapy treatment video/imagery, there is no ethics, privacy, or clinical-data-handling statement and no accessibility documentation; `presentation/Hackathon Presentation.pptx` is an empty (0-byte) placeholder, and no maintenance/archival plan is documented. |
| | **Total** | **25 / 100** | |

## Evidence-backed recommendations

Each recommendation below cites one directly observed repository fact (with its public GitHub URL)
and one pinned _The Turing Way_ chapter retrieved via the required evidence tools.

1. **Add a project scope/purpose section.** Expand `README.md` with the research question, intended
   users, and known limitations, following [Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md).
   Evidence: [`README.md`](https://github.com/stjude-biohackathon/KIDS25-Team3/blob/da0c26763f5d6097e78fea1ec1bb992afedc364d/README.md) is a one-line title with a script pipeline only.
2. **Tag stable releases.** Use annotated Git tags/GitHub releases at meaningful milestones per
   [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md).
   Evidence: history has 52 commits with PR merges but `git tag` is empty ([commit history](https://github.com/stjude-biohackathon/KIDS25-Team3/blob/da0c26763f5d6097e78fea1ec1bb992afedc364d/README.md)).
3. **Publish contribution and conduct guidance.** Add `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and
   issue/PR templates, following [Collaboration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/collaboration.md).
   Evidence: no such files exist in the tree ([README.md](https://github.com/stjude-biohackathon/KIDS25-Team3/blob/da0c26763f5d6097e78fea1ec1bb992afedc364d/README.md) as the closest onboarding doc).
4. **Fix and document the dependency environment.** Re-save `requirements.txt` as UTF-8 and add
   setup instructions, per [Reproducible Environments](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/renv.md).
   Evidence: [`requirements.txt`](https://github.com/stjude-biohackathon/KIDS25-Team3/blob/da0c26763f5d6097e78fea1ec1bb992afedc364d/requirements.txt) is UTF-16LE encoded with CRLF terminators.
5. **Document data/workflow provenance.** Describe dataset sources, schema, and generated-artifact
   handling alongside `data/yaml.yaml`, per [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md)
   (data provenance guidance). Evidence: [`data/yaml.yaml`](https://github.com/stjude-biohackathon/KIDS25-Team3/blob/da0c26763f5d6097e78fea1ec1bb992afedc364d/data/yaml.yaml) has no accompanying documentation.
6. **Add automated tests.** Replace the manual `src/test.py` inference script with an automated
   test suite, per [Code Testing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing.md).
   Evidence: [`src/test.py`](https://github.com/stjude-biohackathon/KIDS25-Team3/blob/da0c26763f5d6097e78fea1ec1bb992afedc364d/src/test.py) only runs a manual model prediction and prints results.
7. **Set up continuous integration.** Add a CI workflow (e.g. GitHub Actions) to run checks on each
   change, per [Continuous Integration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md).
   Evidence: no `.github` directory exists; [`data/yaml.yaml`](https://github.com/stjude-biohackathon/KIDS25-Team3/blob/da0c26763f5d6097e78fea1ec1bb992afedc364d/data/yaml.yaml) is the only YAML file and is unrelated to CI.
8. **Expand usability documentation.** Document installation, the GUI application, and script usage
   in `README.md`, per [Communication](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/communication/communication.md).
   Evidence: [`README.md`](https://github.com/stjude-biohackathon/KIDS25-Team3/blob/da0c26763f5d6097e78fea1ec1bb992afedc364d/README.md) never mentions `gui.py` or the `scripts/` tools.
9. **Add citation and third-party attribution.** Add a `CITATION.cff` and attribution notes for
   dependencies/media, per [Licensing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/licensing.md).
   Evidence: [`LICENSE`](https://github.com/stjude-biohackathon/KIDS25-Team3/blob/da0c26763f5d6097e78fea1ec1bb992afedc364d/LICENSE) is present but no citation/attribution file exists.
10. **Add ethics, accessibility, and sustainability notes.** Document data-handling/privacy
    considerations for clinical treatment media and a maintenance plan, per
    [Ethical Research](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/ethical-research/ethical-research.md).
    Evidence: [`presentation/Hackathon Presentation.pptx`](https://github.com/stjude-biohackathon/KIDS25-Team3/blob/da0c26763f5d6097e78fea1ec1bb992afedc364d/presentation/Hackathon%20Presentation.pptx) is an empty 0-byte placeholder with no ethics/accessibility statement elsewhere.

## Pinned Turing Way citations used in this review

| Resource ID | Title | Source URL |
|---|---|---|
| `turing-way:book/website/project-design/project-design` | Project Design | https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md |
| `turing-way:book/website/reproducible-research/vcs` | Version Control | https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md |
| `turing-way:book/website/collaboration/collaboration` | Collaboration | https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/collaboration.md |
| `turing-way:book/website/reproducible-research/renv` | Reproducible Environments | https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/renv.md |
| `turing-way:book/website/reproducible-research/testing` | Code Testing | https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing.md |
| `turing-way:book/website/reproducible-research/ci` | Continuous Integration | https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md |
| `turing-way:book/website/communication/communication` | Communication | https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/communication/communication.md |
| `turing-way:book/website/reproducible-research/licensing` | Licensing | https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/licensing.md |
| `turing-way:book/website/ethical-research/ethical-research` | Ethical Research | https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/ethical-research/ethical-research.md |
| `turing-way:book/website/LICENSE` | License | https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/LICENSE.md |

## Limitations

- This review only inspected files present in the local checkout of the `main` branch at the
  commit noted above; it did not run the code, execute `gui.py`, train a model, or access any
  GitHub-hosted Issues/Discussions/Wiki content outside the Git repository itself.
- Scores reflect a hackathon-stage research prototype and are not a judgment of the underlying
  scientific or clinical validity of the range-shifter detection approach.
- No credentials, PHI, or restricted files were accessed or referenced in this review.

**This is a Turing Way-aligned readiness snapshot — not an official Turing Way certification.**
