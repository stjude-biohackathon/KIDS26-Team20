# Turing Way-aligned Readiness Snapshot

> **This is not an official certification.** It is a transparent, evidence-based readiness snapshot informed by The Turing Way public guidance; The Turing Way is not represented as a certification authority.

**Review date:** 2026-09-18  
**Repository scope:** public files and Git history in `stjude-biohackathon/KIDS25-Team8_cmdsaw` at commit [`5362e9fa10adec4ed642959e178688000dccce88`](https://github.com/stjude-biohackathon/KIDS25-Team8_cmdsaw/tree/5362e9fa10adec4ed642959e178688000dccce88)  
**Scoring:** 0 = no reliable observable evidence; 5 = partial or inconsistently documented practice; 10 = clear, repeatable, maintained practice. Scores are unweighted integers.

## Readiness score

| # | Criterion | Score (0-10) | Observable repository evidence | Reason for score |
|---|---|---:|---|---|
| 1 | Project purpose and scope | 6 | [README](https://github.com/stjude-biohackathon/KIDS25-Team8_cmdsaw/blob/5362e9fa10adec4ed642959e178688000dccce88/README.md) explains the LLM CLI-help parser, WDL outputs, core functions, and a planned Nextflow feature. | Purpose and broad scope are clear, but intended users, success measures, maintenance scope, and known limitations are not explicitly defined. |
| 2 | Version control and provenance | 5 | The commit-pinned repository has meaningful feature/fix history and four distinct authors in the inspected history. | Git provenance is present, but no tags, release artifacts, changelog, or documented release process is tracked. |
| 3 | Open collaboration | 2 | README invites issues and pull requests. | No tracked contribution guide, code of conduct, maintainer list, review expectations, governance, or discussion path was found. |
| 4 | Reproducible environments | 5 | [pyproject.toml](https://github.com/stjude-biohackathon/KIDS25-Team8_cmdsaw/blob/5362e9fa10adec4ed642959e178688000dccce88/pyproject.toml) declares Python >=3.10 and dependencies; README documents Ollama setup. | Setup is documented, but dependency ranges are not locked and no environment file, container, or supported-platform matrix is tracked. |
| 5 | Data and workflow provenance | 6 | README describes command-help input, JSON documentation, WDL task output, and examples; Pydantic schemas and tests are tracked. | Data sources, generated-artifact retention, metadata/provenance fields, and workflow execution examples are not fully documented. |
| 6 | Testing and validation | 6 | Ten tracked Python test modules cover schemas, WDL generation, providers, and edge cases; `tests/fixtures/fake_help.txt` is a representative fixture. | No public test command is documented in README, the end-to-end test is a placeholder, and no coverage/acceptance threshold is visible. |
| 7 | Automation and continuous integration | 0 | No tracked `.github/workflows/` or other CI configuration was found. | No visible automation runs tests, packaging checks, or reproducibility checks for contributors. |
| 8 | Documentation and usability | 7 | README provides prerequisites, installation, quick start, CLI options, interactive-review explanations, outputs, and troubleshooting. | Documentation has no versioning/support policy and does not separately document developer workflow or limitations in a consolidated way. |
| 9 | Licensing, attribution, and responsible reuse | 6 | [MIT LICENSE](https://github.com/stjude-biohackathon/KIDS25-Team8_cmdsaw/blob/5362e9fa10adec4ed642959e178688000dccce88/LICENSE) is tracked; README contains plain-text citation guidance. | No `CITATION.cff`, DOI/archive, release citation, or third-party attribution inventory is tracked. |
| 10 | Ethics, accessibility, and sustainability | 1 | README identifies local Ollama as an option, which can reduce reliance on cloud inference. | No ethics/privacy guidance, accessibility statement, resource-use policy, archival plan, or maintenance/succession plan was found. |
|  | **Total** | **44 / 100** |  | **Early-stage readiness: practical user documentation, testing, and licensing exist; repeatable automation, collaboration, release, and sustainability practices need attention.** |

## Checks performed

- Reviewed public tracked repository documentation, package metadata, tests, `.gitignore`, and Git history at the pinned commit.
- Confirmed 10 tracked Python test modules and one tracked fixture.
- Confirmed no tracked CI workflow, contribution guide, code of conduct, governance file, citation metadata, changelog, environment lockfile, or Git tag.
- Used the required Turing Way MyGPT evidence workflow: readiness retrieval, resource discovery, direct retrieval of relevant pinned guidance, and one focused evidence packet for each recommendation below.

## Citation-backed recommendations

Repository observations are kept separate from the recommendations. Each link below is a pinned Turing Way source resolved by the evidence service.

1. **Publish a roadmap and changelog.** The README names a planned feature, but no roadmap or changelog is tracked. [The Turing Way: Project Documentation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md) identifies both as core project documentation.
2. **Make collaboration explicit.** Add `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, maintainer contacts, and concise review expectations. The repository currently only invites issues and pull requests. [The Turing Way: Collaboration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/collaboration.md) emphasizes contribution-friendly, inclusive collaboration and clear expectations.
3. **Make the software citable.** Add `CITATION.cff` and archive a tagged release to establish persistent citation metadata; the current README citation is plain text only. [The Turing Way: Project Documentation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md) specifically recommends `CITATION.cff`.
4. **Capture a repeatable environment.** Preserve a tested dependency resolution and document supported platforms; the project currently has dependency ranges and setup instructions but no lockfile/environment capture. [The Turing Way: Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md) calls for explicit resources, constraints, and usable project setup.
5. **Add visible CI and meaningful end-to-end validation.** Run the existing tests on pull requests and the default branch, then replace the placeholder end-to-end test with a deterministic mocked workflow path. The repository has tests but no CI. [The Turing Way: Research Infrastructure Developer](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/research-infrastructure-roles/research-infrastructure-developer.md) describes version control and continuous integration/deployment as practices for maintainable research infrastructure.

## Evidence sources

- [The Turing Way: Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md)
- [The Turing Way: Project Documentation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md)
- [The Turing Way: Collaboration](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/collaboration.md)
- [The Turing Way: Research Infrastructure Developer](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/research-infrastructure-roles/research-infrastructure-developer.md)

## Confidence and limitations

**Confidence: moderate (7/10).** Scores are strongly supported by files present or absent in the commit-pinned public tree and by the relevant MyGPT retrievals. This review did not inspect GitHub repository settings, issue/PR discussions, external package registries, release archives, branch protections, unpublished policies, or private operational practices. Therefore, no score is a claim that an unobserved practice does or does not exist elsewhere.
