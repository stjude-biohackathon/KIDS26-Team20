# Turing Way-Aligned Readiness Snapshot

**This is a Turing Way-aligned readiness review produced with automated
assistance. It is not an official Turing Way certification, and The Turing
Way is not a certification authority.** No institution or governing body has
authorized this report as a compliance or certification decision. Treat it as
a transparent, evidence-based snapshot of observable practices, not a
guarantee of quality or an endorsement.

- **Repository:** [stjude-biohackathon/KIDS25-Team13](https://github.com/stjude-biohackathon/KIDS25-Team13)
- **Reviewed commit:** `cb4d02b72f33d67c8f12ba9a78963574fc524e1f` (branch `main`)
- **Review date:** 2026-09-18
- **Scope:** Publicly accessible repository contents (root files, commit
  history, issues/pull requests, releases, and GitHub Actions configuration)
  as of the reviewed commit. No private or non-public information was
  inspected.
- **Confidence:** High — the repository is extremely small (two files, one
  commit), so observable evidence is unambiguous and easy to verify directly
  against the GitHub API and checkout.

## Method

Evidence was gathered directly from the repository (file listing, `git log`,
`gh api` calls for issues, pull requests, releases, branches, and Actions
workflows) and cross-referenced against pinned guidance retrieved from *The
Turing Way* via the required learning-assistant evidence tools
(`get_turing_way_review_evidence` and `get_turing_way_evidence_packets`,
backed by `list_resources`/`get_resource`). Each row below cites one directly
observed repository fact and one pinned Turing Way chapter. Scores use the
ten-criterion, 0–10 rubric (10 criteria × 10 points = 100 total); 0 means no
reliable evidence was found, 5 means the practice is partially or
inconsistently documented, and 10 means the practice is clear, repeatable,
and maintained.

## Score table

| # | Criterion | Score (/10) | Observed repository evidence | Turing Way guidance |
|---|-----------|:-----------:|-------------------------------|----------------------|
| 1 | Project purpose and scope | 0 | [README.md](https://github.com/stjude-biohackathon/KIDS25-Team13/blob/cb4d02b72f33d67c8f12ba9a78963574fc524e1f/README.md) is a single 15-byte line, `# KIDS25-Team13`, with no research question, scope, intended users, or known limitations. | [Guide for Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md) |
| 2 | Version control and provenance | 1 | The [`main` branch](https://github.com/stjude-biohackathon/KIDS25-Team13/commit/cb4d02b72f33d67c8f12ba9a78963574fc524e1f) has a single "Initial commit," no tags or releases exist, and [PR #1](https://github.com/stjude-biohackathon/KIDS25-Team13/pull/1) ("Added CLAUDE.md") is open and unmerged. | [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md) |
| 3 | Open collaboration | 1 | Issues/PRs are enabled and one PR is in progress, but the [repository tree](https://github.com/stjude-biohackathon/KIDS25-Team13/tree/cb4d02b72f33d67c8f12ba9a78963574fc524e1f) has no CONTRIBUTING.md, CODE_OF_CONDUCT.md, issue templates, or PR templates. | [Maintaining and Reviewing Contributions](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/maintain-review/maintain-review-review.md) |
| 4 | Reproducible environments | 0 | The [repository root](https://github.com/stjude-biohackathon/KIDS25-Team13/tree/cb4d02b72f33d67c8f12ba9a78963574fc524e1f) contains only `LICENSE` and `README.md`; no dependency manifest, environment file, or setup instructions exist. | [Overcoming Barriers to Reproducible Research](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/overview/overview-barriers.md) |
| 5 | Data and workflow provenance | 0 | No data directory, workflow files, or scripts exist anywhere in the [repository tree](https://github.com/stjude-biohackathon/KIDS25-Team13/tree/cb4d02b72f33d67c8f12ba9a78963574fc524e1f). | [Metadata for Data Management](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm/rdm-metadata.md) |
| 6 | Testing and validation | 0 | No test files, test directories, or documented validation instructions exist in the [repository tree](https://github.com/stjude-biohackathon/KIDS25-Team13/tree/cb4d02b72f33d67c8f12ba9a78963574fc524e1f). | [Testing Guidance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-guidance.md) |
| 7 | Automation and continuous integration | 0 | The GitHub Actions [workflows API](https://github.com/stjude-biohackathon/KIDS25-Team13/tree/cb4d02b72f33d67c8f12ba9a78963574fc524e1f) returns an empty list; there is no `.github/workflows` directory or CI configuration. | [Continuous Integration Practices](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci/ci-practices.md) |
| 8 | Documentation and usability | 0 | [README.md](https://github.com/stjude-biohackathon/KIDS25-Team13/blob/cb4d02b72f33d67c8f12ba9a78963574fc524e1f/README.md) contains only a title heading, with no usage, installation, or onboarding content. | [Code Documentation for Projects](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md) |
| 9 | Licensing, attribution, and responsible reuse | 6 | An [MIT `LICENSE`](https://github.com/stjude-biohackathon/KIDS25-Team13/blob/cb4d02b72f33d67c8f12ba9a78963574fc524e1f/LICENSE) file is present and unambiguous, but no `CITATION.cff` or other citation/attribution guidance exists. | [Licensing FLOSS Projects](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/licensing/licensing-floss.md) |
| 10 | Ethics, accessibility, and sustainability | 0 | No ethics statement, accessibility notes, or sustainability/maintenance plan appear anywhere in the [repository](https://github.com/stjude-biohackathon/KIDS25-Team13/tree/cb4d02b72f33d67c8f12ba9a78963574fc524e1f). | [Governance in Open Source Projects](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/ethical-research/ethics-open-source-governance.md) |

**Total: 8 / 100**

## Recommendations

1. Write a real README covering the project's research question, scope,
   intended users, and known limitations (cites *Project Design*).
2. Merge or close the pending pull request and adopt an incremental commit
   and tagging/release practice going forward (cites *Version Control*).
3. Add `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and issue/PR templates to set
   expectations for contributors (cites *Maintaining and Reviewing
   Contributions*).
4. Add setup instructions and a pinned dependency/environment manifest
   (e.g., `requirements.txt`, `environment.yml`, or a container definition)
   (cites *Overcoming Barriers to Reproducible Research*).
5. Document any data sources, schemas, and workflow steps once code or data
   are added (cites *Metadata for Data Management*).
6. Add automated or documented tests with clear instructions for reproducing
   checks (cites *Testing Guidance*).
7. Add a CI workflow (e.g., GitHub Actions) so checks run automatically and
   failures are visible to contributors (cites *Continuous Integration
   Practices*).
8. Expand documentation with usage examples and an onboarding path as the
   project grows (cites *Code Documentation for Projects*).
9. Add a `CITATION.cff` file to complement the existing MIT license and
   clarify reuse/citation expectations (cites *Licensing FLOSS Projects*).
10. Add a short statement on ethical considerations, accessibility, and a
    sustainability/maintenance plan (cites *Governance in Open Source
    Projects*).

## Limitations

- The repository consists of only two files (`LICENSE`, `README.md`) and one
  commit at the time of review; most criteria could not be evaluated beyond
  their absence.
- Private repository data, non-public discussions, and any external
  infrastructure (e.g., private CI, private data stores) were not accessible
  and were not assumed to exist.
- This snapshot reflects the reviewed commit only and will not update
  automatically as the repository changes.
- This is not an official Turing Way certification; it is guidance-aligned
  and produced with automated assistance, for the team's own use in
  improving research-software practice.
