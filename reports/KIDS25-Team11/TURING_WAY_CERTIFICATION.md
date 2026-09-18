# Turing Way Readiness Snapshot — KIDS25-Team11

> **This is a Turing Way-aligned readiness snapshot, not an official
> certification.** The Turing Way is public best-practice guidance, not a
> certification authority or institutional policy. No official body has
> reviewed or endorsed this repository. Scores reflect only what is
> observable in the public repository at the reviewed commit; they are not
> legal, ethical, security, or institutional approval.

## Review metadata

- **Repository:** [`stjude-biohackathon/KIDS25-Team11`](https://github.com/stjude-biohackathon/KIDS25-Team11)
- **Reviewed commit:** [`5bda7ab4a71331a4ec0126a865fd8a0c8c557d28`](https://github.com/stjude-biohackathon/KIDS25-Team11/commit/5bda7ab4a71331a4ec0126a865fd8a0c8c557d28) (`main`, "Update README.md")
- **Review date:** 2026-09-18
- **Scope:** Public repository contents only — the R Shiny application
  (`HartwellV20/app.R`, `server.R`, `ui.R`), top-level R scripts, `README.md`,
  `LICENSE`, and repository/version-control metadata. No private data,
  credentials, or non-public information were accessed.
- **Confidence:** Medium — the repository is small (8 commits, ~9 files) and
  was fully enumerated, so observations are reliable; however, no maintainer
  interviews or issue/PR history beyond the default branch were reviewed.

## Total score: **17 / 100**

## Ten-criterion score table

| # | Criterion | Score (0–10) | Evidence (repository) | Turing Way guidance cited |
|---|-----------|:---:|---|---|
| 1 | Project purpose and scope | 4 | [`README.md`](https://github.com/stjude-biohackathon/KIDS25-Team11/blob/5bda7ab4a71331a4ec0126a865fd8a0c8c557d28/README.md) states the app's purpose (a Shared Resource Form Generator for sequencing orders) and its two service options, but documents no scope boundary, target-user detail, or known limitations. | [Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md) |
| 2 | Version control and provenance | 2 | Commit history at [`/commits`](https://github.com/stjude-biohackathon/KIDS25-Team11/commits/5bda7ab4a71331a4ec0126a865fd8a0c8c557d28) shows 8 commits, most titled generically "Add files via upload"; no tags or releases exist. | [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md) |
| 3 | Open collaboration | 0 | [Repository root](https://github.com/stjude-biohackathon/KIDS25-Team11/tree/5bda7ab4a71331a4ec0126a865fd8a0c8c557d28) has no `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, or `.github/ISSUE_TEMPLATE`; no contribution or review path is documented. | [Code of Conduct](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/coc.md) |
| 4 | Reproducible environments | 1 | [`HartwellV20/app.R`](https://github.com/stjude-biohackathon/KIDS25-Team11/blob/5bda7ab4a71331a4ec0126a865fd8a0c8c557d28/HartwellV20/app.R) is an R Shiny app with no `DESCRIPTION`, `renv.lock`, or other dependency manifest, and `README.md` gives no setup/installation instructions. | [Reproducible Research](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/reproducible-research.md) |
| 5 | Data and workflow provenance | 1 | [`CAB empty dataframes.R`](https://github.com/stjude-biohackathon/KIDS25-Team11/blob/5bda7ab4a71331a4ec0126a865fd8a0c8c557d28/CAB%20empty%20dataframes.R) and `Sequencingt empty dataframes.R` build and manipulate order dataframes, with no documentation of data sources, schemas, or expected input/output formats. | [Research Data Management](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm.md) |
| 6 | Testing and validation | 0 | No `tests/` directory or files matching `test*` exist anywhere in the [repository tree](https://github.com/stjude-biohackathon/KIDS25-Team11/tree/5bda7ab4a71331a4ec0126a865fd8a0c8c557d28); no validation criteria are documented. | [Testing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing.md) |
| 7 | Automation and continuous integration | 0 | No `.github/workflows` directory or other CI configuration exists in the [repository tree](https://github.com/stjude-biohackathon/KIDS25-Team11/tree/5bda7ab4a71331a4ec0126a865fd8a0c8c557d28); no automated checks run on changes. | [Continuous Integration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md) |
| 8 | Documentation and usability | 3 | `README.md` is a short two-paragraph description with no usage walkthrough; the repository also contains an unprofessionally named artifact, [`The Broken Html Code :(`](https://github.com/stjude-biohackathon/KIDS25-Team11/blob/5bda7ab4a71331a4ec0126a865fd8a0c8c557d28/The%20Broken%20Html%20Code%20%3A%28), indicating limited documentation polish. | [Project Design Overview](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/pd-overview.md) |
| 9 | Licensing, attribution, and responsible reuse | 6 | An MIT [`LICENSE`](https://github.com/stjude-biohackathon/KIDS25-Team11/blob/5bda7ab4a71331a4ec0126a865fd8a0c8c557d28/LICENSE) file is present, attributing copyright to St. Jude Children's Research Hospital BioHackathon (2025); however, there is no `CITATION.cff` or citation/attribution guidance for reuse. | [License](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/LICENSE.md) |
| 10 | Ethics, accessibility, and sustainability | 0 | Neither [`README.md`](https://github.com/stjude-biohackathon/KIDS25-Team11/blob/5bda7ab4a71331a4ec0126a865fd8a0c8c557d28/README.md) nor any other file discusses ethical/privacy considerations for sequencing-order data, accessibility, or a maintenance/archival plan. | [Legal Disclaimer](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/legal-disclaimer.md) |
| | **Total** | **17 / 100** | | |

## Observed repository facts (checks performed)

- Repository contents at the reviewed commit: `README.md`, `LICENSE`,
  `server.R`, `ui.R`, `HartwellV20/app.R`, `CAB empty dataframes.R`,
  `Sequencingt empty dataframes.R`, `St Jude Website Test 3.html`, and
  `The Broken Html Code :(`.
- `git log` at the reviewed commit shows 8 commits from 5 authors, spanning
  2025-08-24 to 2025-10-01; 5 of 8 commits are titled "Add files via upload"
  (GitHub web-upload default message) and `git tag` returns no tags.
- No `.github/` directory (no CI workflows, no issue/PR templates) exists in
  the repository.
- No `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff`, `DESCRIPTION`,
  or `renv.lock` file exists in the repository.
- No `tests/` directory or test files exist in the repository.

## Recommendations (ranked by impact)

1. **Add automated tests and a CI workflow** (criteria 6–7, currently 0/10
   each). Even a minimal `.github/workflows/` job that runs `R CMD check` or
   loads `app.R`/`server.R`/`ui.R` to catch syntax errors would substantially
   raise reproducibility confidence. See The Turing Way's
   [Testing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing.md)
   and [CI](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md)
   guidance.
2. **Declare and pin dependencies** (criterion 4, 1/10). Add an R
   `DESCRIPTION` file or `renv.lock` and README setup instructions so others
   can reproduce the Shiny app's environment. See
   [Reproducible Research](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/reproducible-research.md).
3. **Add open-collaboration documentation** (criterion 3, 0/10): a
   `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` clarify how others can
   contribute and what conduct is expected. See
   [Code of Conduct](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/coc.md).
4. **Document data provenance** (criterion 5, 1/10): describe the source,
   schema, and expected shape of the dataframes the R scripts construct. See
   [Research Data Management](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm.md).
5. **Improve commit hygiene and documentation** (criteria 2 and 8): use
   descriptive commit messages and tag releases; expand the README with
   setup/usage instructions and remove or rename ad hoc artifacts such as
   `The Broken Html Code :(`.
6. **Add ethics/accessibility/sustainability notes** (criterion 10, 0/10):
   state whether the form handles any sensitive data, and note a maintenance
   plan. See [Legal Disclaimer](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/legal-disclaimer.md).

## Limitations of this snapshot

- This snapshot reflects only the public repository contents at the pinned
  commit above; it does not assess private issues, discussions, forks,
  security posture, or institutional/legal compliance.
- Scores are based on presence/absence of observable artifacts and their
  content, not on runtime testing of the Shiny application.
- This is **not** an official Turing Way certification, and The Turing Way
  project does not issue certifications. Treat this as guidance-aligned
  self-assessment input only.
