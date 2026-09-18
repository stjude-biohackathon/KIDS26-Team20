# Turing Way-aligned readiness snapshot

> **Not an official certification.** This is a transparent, repository-only
> readiness snapshot informed by The Turing Way public best-practice guidance.
> The Turing Way is not represented as a certification authority.

## Review details

| Item | Value |
|---|---|
| Review date | 2026-09-18 |
| Scope | Public, tracked contents of `stjude-biohackathon/KIDS25-Team8_flowjomojo` at commit `1d005ca3f45cf0fca0a2e791b54e4913c9f3beb7` |
| Method | Observable repository evidence plus pinned Turing Way guidance; no hidden, sensitive, or external project materials reviewed |
| Confidence | Moderate (7/10): repository content was accessible and inspected, but deployment, GitHub settings, and untracked team practices were out of scope |
| Total | **37 / 100** |

## Score table

Scores are integers from 0 to 10. A score of 0 means no reliable repository
evidence was found; 5 denotes partial or inconsistent evidence; 10 denotes
clear, repeatable, maintained evidence.

| # | Criterion | Score / 10 | Observable repository evidence | Readiness reason |
|---:|---|---:|---|---|
| 1 | Project purpose and scope | 7 | `README.md` describes a browser-based ReactFlow app for generating Nextflow/WDL pipelines and gives a visual Quick Start. | Purpose and core audience are clear, but known limitations are not stated. |
| 2 | Version control and provenance | 5 | The Git history contains descriptive implementation commits. No tags or release metadata were found. | Change history is meaningful, but release and version provenance are not documented. |
| 3 | Open collaboration | 1 | No `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, governance guide, issue/discussion path, review expectations, or maintainer information was found. | Public collaboration expectations and routes are largely absent. |
| 4 | Reproducible environments | 5 | `package.json` and `package-lock.json` declare the JavaScript dependencies and provide `build`/`lint` scripts. | Dependency capture is present, but no installation, supported-version, or environment setup guidance is documented. |
| 5 | Data and workflow provenance | 4 | `README.md` identifies the commands JSON location and shows an informal schema. | The bundled `commands.json` lacks source version, license, refresh process, and generated-artifact provenance. |
| 6 | Testing and validation | 2 | `package.json` offers lint and build commands; no test script or tracked test files were found. | Basic static/build checks exist, but automated behavioral validation and reproduction instructions are absent. |
| 7 | Automation and continuous integration | 0 | No GitHub Actions workflow or other tracked CI configuration was found. | No visible automation runs quality or reproducibility checks for contributors. |
| 8 | Documentation and usability | 7 | `README.md` provides features, a four-step visual walkthrough, and commands JSON documentation. | Strong user-facing overview, but local installation and developer onboarding instructions are missing. |
| 9 | Licensing, attribution, and responsible reuse | 6 | The root `LICENSE` is MIT. No `CITATION.cff`, preferred citation, or third-party attribution inventory was found. | Reuse terms are clear, but scholarly attribution and dependency/data attribution are incomplete. |
| 10 | Ethics, accessibility, and sustainability | 0 | No ethics, privacy, accessibility, sustainability, archival, or maintenance-plan documentation was found. | No reliable evidence supports these project practices in the reviewed contents. |

## Evidence and pinned Turing Way guidance

The following recommendations are separate from the observed facts above. Each
is grounded in an evidence packet retrieved from the Turing Way source pinned
at commit `bb3f7abb56a40cd92a654fb51e4ec91f429cca2a`.

| Readiness recommendation | Direct repository observation | Pinned Turing Way guidance |
|---|---|---|
| State intended users, scope boundaries, and known limitations in the README. | The purpose and workflow features are documented, but limitations are absent. | [Accessible and equitable communication](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/communication/aa.md) |
| Create tagged releases and describe version/release provenance. | Meaningful commits exist, but tags and release metadata were not found. | [Maintaining and reviewing projects](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/maintain-review.md) |
| Add contribution, conduct, governance, maintainer, and support-path documentation. | No such project files or README sections were found. | [Guidance for new communities](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/new-community/new-community-guide.md) |
| Document local setup, supported Node.js versions, and dependency update practice. | Dependencies are declared and locked, but setup and version guidance are absent. | [Project maintenance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/maintain-review/maintain-review-maintenance.md) |
| Record `commands.json` source, version, license, schema, and refresh process. | The file is shipped with an informal README schema but no provenance metadata. | [Data usage statement](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/afterword/data-usage-statement.md) |
| Add representative automated tests and document how to run them. | Lint and build scripts exist, but no tests or test command were found. | [Code review practices](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/maintain-review/maintain-review-review.md) |
| Add visible CI for lint, build, and the new test suite. | No CI configuration was found. | [Project maintenance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/maintain-review/maintain-review-maintenance.md) |
| Add installation and developer-onboarding documentation. | The README offers user workflow guidance but no local setup path. | [Accessible and equitable communication](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/communication/aa.md) |
| Add a `CITATION.cff` and third-party/data attribution inventory. | MIT licensing is present; citation and attribution materials are absent. | [License](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/LICENSE.md) |
| Document relevant accessibility, privacy/ethics, maintenance, and archival commitments. | No documentation of these areas was found. | [Equitable communication](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/communication/aa/aa-equitable.md) |

## Checks and limitations

The review inspected the tracked source tree, README, license, package metadata
and lockfile, utility code, Git history, and the absence of test, CI,
contribution, conduct, governance, citation, and data-management files. It
does not assess GitHub-hosted settings, deployment configuration, untracked
materials, organizational policies, or practices that are not observable in
this public repository.

The score is a readiness signal, not a certification decision or an assertion
of Turing Way compliance.
