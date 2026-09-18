# Turing Way-Aligned Readiness Snapshot

> **This is not an official certification.** The Turing Way is public
> best-practice guidance, not a certification authority or institutional
> policy. This document is a transparent, evidence-based readiness snapshot
> against a ten-criterion rubric inspired by *The Turing Way*, produced for
> internal reference only.

- **Review date:** 2026-09-18
- **Repository reviewed:** [`stjude-biohackathon/KIDS25-Team19`](https://github.com/stjude-biohackathon/KIDS25-Team19)
- **Commit reviewed:** `a836a1fd76c528fa7cf4785ef67817ee2a612647` (branch `main`)
- **Scope:** Entire public repository as committed at the reviewed commit — `README.md`, `LICENSE`, `global.R`, `server.R`, `ui.R`. No other files, directories, or hidden configuration were present.
- **Confidence:** Moderate-to-high. The repository is small (5 files, 2 commits) and every observation below was made directly against files present at the reviewed commit; absence claims (no tests, no CI, no CONTRIBUTING, etc.) are high confidence, while the version-control and licensing scores carry moderate confidence due to limited history to judge trends from.
- **Total score: 11 / 100**

## Ten-criterion rubric (0–10 each, 100 total)

| # | Criterion | Score | Evidence (repository fact) | Turing Way guidance cited |
|---|-----------|:-----:|-----------------------------|----------------------------|
| 1 | Project purpose and scope | 0/10 | [`README.md`](https://github.com/stjude-biohackathon/KIDS25-Team19/blob/a836a1fd76c528fa7cf4785ef67817ee2a612647/README.md) exists but contains 0 lines of content; no other document states the project's purpose, scope, intended users, or limitations. | [Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md) |
| 2 | Version control and provenance | 2/10 | `git log` shows only two commits (`Initial commit`, `Initial code commit`) and `git tag` returns no tags as of `a836a1f`; history exists but carries no descriptive messages, tags, or releases. | [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md) |
| 3 | Open collaboration | 0/10 | A repository-wide search of the tree at `a836a1f` finds no `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, or `.github/` issue templates in the repository root. | [New Community Tech Issues](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/new-community/new-community-techissues.md) |
| 4 | Reproducible environments | 1/10 | [`global.R`](https://github.com/stjude-biohackathon/KIDS25-Team19/blob/a836a1fd76c528fa7cf4785ef67817ee2a612647/global.R) lists 19 `library()` calls with no version pins, and the repository has no `renv.lock`, `Dockerfile`, or `environment.yml`. | [Renv Package](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/renv/renv-package.md) |
| 5 | Data and workflow provenance | 1/10 | [`server.R`](https://github.com/stjude-biohackathon/KIDS25-Team19/blob/a836a1fd76c528fa7cf4785ef67817ee2a612647/server.R) queries an `authControl.db` SQLite database and calls internal endpoints (e.g. `apis-research.stjude.org/srmapi`) with no schema, sample data, or provenance documentation checked into the repo. | [RDM Checklist](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm/rdm-checklist.md) |
| 6 | Testing and validation | 0/10 | The repository tree at `a836a1f` contains only `global.R`, `server.R`, `ui.R`, `README.md`, and `LICENSE`; there is no `tests/` directory, `testthat` file, or documented test procedure. | [Testing Guidance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-guidance.md) |
| 7 | Automation and continuous integration | 0/10 | No `.github/workflows` directory or any other CI configuration file exists in the repository tree at `a836a1f`. | [Continuous Integration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md) |
| 8 | Documentation and usability | 1/10 | [`README.md`](https://github.com/stjude-biohackathon/KIDS25-Team19/blob/a836a1fd76c528fa7cf4785ef67817ee2a612647/README.md) has 0 lines of content, and no other documentation file (`docs/`, wiki, or usage guide) exists; a small amount of in-app help text exists inside `server.R`'s `output$tokens`. | [Code Documentation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md) |
| 9 | Licensing, attribution, and responsible reuse | 6/10 | [`LICENSE`](https://github.com/stjude-biohackathon/KIDS25-Team19/blob/a836a1fd76c528fa7cf4785ef67817ee2a612647/LICENSE) contains the full MIT License text with copyright "(c) 2025 St. Jude Children's Research Hospital BioHackathon"; there is no `CITATION.cff` or third-party attribution notice for the bundled R packages. | [Licensing (FLOSS)](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/licensing/licensing-floss.md) |
| 10 | Ethics, accessibility, and sustainability | 0/10 | [`server.R`](https://github.com/stjude-biohackathon/KIDS25-Team19/blob/a836a1fd76c528fa7cf4785ef67817ee2a612647/server.R) processes user, PI, and department personal data retrieved from internal St. Jude APIs and sends email, with no privacy, accessibility, or maintenance/archival statement in any repository file. | [Ethics and Open Source Governance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/ethical-research/ethics-open-source-governance.md) |

**Total: 11 / 100**

## Checks performed

- Listed the full repository tree at the reviewed commit (`README.md`, `LICENSE`, `global.R`, `server.R`, `ui.R`; no hidden directories).
- Read `README.md` (0 lines), `LICENSE` (MIT, full text), `global.R` (dependency list), `server.R` (250 lines), and `ui.R` (61 lines) in full.
- Inspected `git log --oneline`, `git branch -a`, and `git tag` for version-control history.
- Searched for `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/` templates, `.github/workflows/`, `tests/`, `renv.lock`, `Dockerfile`, and `environment.yml` — none were present.
- Retrieved matching *Turing Way* guidance for each criterion via the required learning-assistant evidence tools before scoring.

## Recommendations

1. **Project purpose and scope:** Add a README describing the app's purpose (SRM email templating for St. Jude Shared Resources), intended users, and known limitations, per *Turing Way* project design guidance.
2. **Version control and provenance:** Adopt descriptive commit messages and tag releases as the app stabilizes.
3. **Open collaboration:** Add `CONTRIBUTING.md`, a code of conduct, and clarify maintainership/issue-reporting paths.
4. **Reproducible environments:** Pin package versions (e.g. via `renv::snapshot()`) and commit a lockfile or container definition.
5. **Data and workflow provenance:** Document the `authControl.db` schema, the external SRM/CAGE API contracts, and the email-template token system referenced in `server.R`.
6. **Testing and validation:** Add automated tests (e.g. `testthat`) for the reactive logic in `server.R`, especially department-conditional branches.
7. **Automation and CI:** Add a CI workflow (e.g. GitHub Actions) to lint/check the R code on each change.
8. **Documentation and usability:** Expand the README into setup/usage instructions; the in-app token help text in `server.R` is a good start but is not discoverable outside the running app.
9. **Licensing, attribution, and responsible reuse:** Add a `CITATION.cff` and attribution notes for the third-party R packages the app depends on.
10. **Ethics, accessibility, and sustainability:** Document handling of personal/institutional data (user, PI, department, email), and note a maintenance/archival plan.

## Limitations

- This snapshot reflects only the single commit reviewed (`a836a1f`) on the `main` branch; it does not reflect any later changes.
- Only repository-observable evidence was used; no runtime testing of the Shiny app, no access to `authControl.db` contents, and no verification of the internal St. Jude APIs it calls were performed or attempted.
- Confidence in the exact numeric score for "Version control and provenance" and "Licensing, attribution" is moderate — these are judgment calls within the rubric's 0–10 band rather than binary presence/absence checks.
- This is a readiness snapshot against *The Turing Way*'s published best-practice guidance, not an official Turing Way certification, and carries no legal, institutional, or security-audit weight.
