# Turing Way-aligned readiness snapshot

> **Not an official certification.** This is a transparent, evidence-based
> readiness snapshot aligned with _The Turing Way_; it is not a certification
> by, or on behalf of, _The Turing Way_.

**Repository reviewed:** `stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow`  
**Review scope:** Entire public repository at the commit below; only tracked,
non-sensitive repository material was assessed.  
**Repository revision:** [`272209bf4cc73b4273cea21f52ba3dadada699c7`](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/commit/272209bf4cc73b4273cea21f52ba3dadada699c7)  
**Review date:** 2026-09-18  
**Confidence:** Moderate (7/10)

## Total score: 28 / 100

Each criterion is scored once from 0 to 10 using observable evidence only:
0 = no reliable evidence; 5 = partial or inconsistently documented practice;
10 = clear, repeatable, maintained practice.

| # | Criterion | Score (0-10) | Observable repository evidence | Assessment |
|---|---|---:|---|---|
| 1 | Project purpose and scope | 4 | [README](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/blob/272209bf4cc73b4273cea21f52ba3dadada699c7/README.md) identifies an OnDemand interface for Nextflow and its LSF/HPC constraint. | Basic purpose and a known limitation are clear. Intended users, support boundary, deployment prerequisites, objectives, and success criteria are not documented. |
| 2 | Version control and provenance | 7 | The public [Git history](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/commits/272209bf4cc73b4273cea21f52ba3dadada699c7) records changes; [CHANGELOG.md](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/blob/272209bf4cc73b4273cea21f52ba3dadada699c7/CHANGELOG.md) records version 0.99.0. | Public Git history and a changelog establish useful source provenance. No tagged release, release artifact, or documented provenance process is observable. |
| 3 | Open collaboration | 1 | The project is publicly hosted on GitHub. The [pinned tree](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/tree/272209bf4cc73b4273cea21f52ba3dadada699c7) contains no contribution guide, code of conduct, issue templates, review policy, or maintainership information. | A public repository enables discovery, but contributors have no documented participation path or community norms. |
| 4 | Reproducible environments | 4 | The [job template](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/blob/272209bf4cc73b4273cea21f52ba3dadada699c7/template/script.sh.erb) loads `Nextflow/24.10.2`, specifies a Singularity cache, accepts a pipeline revision and parameters file, and supports resume. | Several runtime controls are explicit. There are no setup instructions, dependency manifest, captured environment, supported platform matrix, or reproducible environment validation. |
| 5 | Data and workflow provenance | 3 | [manifest.yml](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/blob/272209bf4cc73b4273cea21f52ba3dadada699c7/manifest.yml) describes parameter-file input and resume behavior; the [template](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/blob/272209bf4cc73b4273cea21f52ba3dadada699c7/template/script.sh.erb) records the execution workflow. | Input format and core execution steps are partially documented. Input/output schemas, sample data, generated artifacts, data sources, retention, and metadata practices are not published. |
| 6 | Testing and validation | 0 | No test files or test configuration are present in the [pinned tree](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/tree/272209bf4cc73b4273cea21f52ba3dadada699c7). | No automated or documented validation procedure, fixtures, or acceptance criteria are observable. |
| 7 | Automation and continuous integration | 0 | No `.github/workflows` directory or other tracked CI configuration is present in the [pinned tree](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/tree/272209bf4cc73b4273cea21f52ba3dadada699c7). | No contributor-visible automation checks are observable. |
| 8 | Documentation and usability | 3 | The [README](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/blob/272209bf4cc73b4273cea21f52ba3dadada699c7/README.md) and [manifest](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/blob/272209bf4cc73b4273cea21f52ba3dadada699c7/manifest.yml) describe the application at a high level. | The user-facing purpose is understandable, but deployment, configuration, end-to-end use, troubleshooting, examples, and maintenance documentation are absent. |
| 9 | Licensing, attribution, and responsible reuse | 5 | An [MIT License](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/blob/272209bf4cc73b4273cea21f52ba3dadada699c7/LICENSE) is present. No `CITATION.cff`, preferred citation, or third-party attribution inventory is present in the [pinned tree](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/tree/272209bf4cc73b4273cea21f52ba3dadada699c7). | Reuse permissions are clear, but software attribution and citation guidance are incomplete. |
| 10 | Ethics, accessibility, and sustainability | 1 | The [README](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/blob/272209bf4cc73b4273cea21f52ba3dadada699c7/README.md) notes the LSF/HPC limitation. No accessibility statement, ethics/privacy guidance, sustainability plan, archival plan, or maintenance policy is present in the [pinned tree](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow/tree/272209bf4cc73b4273cea21f52ba3dadada699c7). | A material platform limitation is disclosed; no wider responsible-use, access, or long-term stewardship practice is documented. |

## Checks performed

| Check | Result |
|---|---|
| Public tracked-file review | Complete: 10 tracked files, including documentation, templates, manifest, changelog, and license |
| Required learning-assistant review evidence | Retrieved before scoring |
| Pinned Turing Way guidance | Retrieved from immutable `bb3f7abb56a40cd92a654fb51e4ec91f429cca2a` references |
| Score coverage | Complete: exactly 10 criteria, each scored once on a 0-10 scale |
| PDF score-table verification | Complete: the generated PDF is non-empty and text extraction contains all 10 criteria and `28 / 100` |

## Recommendations

1. Add a deployment and user guide covering Open OnDemand/LSF prerequisites,
   supported versions, configuration, a minimal parameters example, expected
   outputs, and troubleshooting.
2. Add template/configuration checks and a representative submission smoke test;
   execute them in pull-request CI.
3. Publish `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, maintainership/support
   details, and issue templates.
4. Add `CITATION.cff` and an attribution inventory for bundled or external
   components.
5. Document accessibility, privacy/ethical boundaries, data handling, and a
   maintenance or archival plan.

## Turing Way evidence and limitations

The learning assistant retrieved the following immutable Turing Way guidance
before scoring and evidence packets were resolved against the pinned repository
revision:

| Turing Way guidance | Relevance to this snapshot |
|---|---|
| [Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md) | Purpose, scope, users, constraints, and project planning |
| [Project Documentation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md) | README, contribution guidance, changelog, license, conduct, and citation |
| [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md) | Traceable, auditable provenance and collaboration |
| [Reproducibility Methods](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/pd-overview/pd-overview-methods.md) | Environment, dependency, infrastructure, and data-management decisions |
| [Accessibility](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/accessibility.md) | Technical and community decisions that reduce barriers to participation |

**Limitations:** This review scores only public, repository-observable
evidence. It does not infer undocumented operational controls, private
infrastructure, untracked documentation, or external support practices. The
score is a readiness signal, not an official Turing Way certification.
