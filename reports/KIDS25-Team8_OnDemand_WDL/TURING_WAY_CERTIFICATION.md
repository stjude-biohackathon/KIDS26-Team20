# Turing Way Readiness Snapshot

**Repository:** `stjude-biohackathon/KIDS25-Team8_OnDemand_WDL`  
**Revision reviewed:** `efcaaf3f17794e304cd1139d84c9b43a1600d06a`  
**Date:** 2026-09-18  
**Status:** Turing Way-aligned readiness snapshot; this is not an official certification.

## Summary

**Total score: 49 / 100 (49%)**  
**Confidence: Moderate.** The score is based on observable repository contents at the pinned revision. The repository is small and easy to inspect, but no executable test or CI evidence is available, and runtime behavior depends on an external OnDemand/HPC environment.

The required MyGPT learning-assistant evidence retrieval was completed before scoring. This is a transparent readiness snapshot, not an official Turing Way certification.

## Ten-criterion score table

| # | Criterion | Score (0-10) | Evidence and rationale |
|---:|---|---:|---|
| 1 | Project purpose and scope | 6 / 10 | `README.md` identifies the OnDemand WDL application, LSF/HPC target, project origin, and limitations, but does not define detailed goals or supported use cases. |
| 2 | Version control and provenance | 7 / 10 | Git history contains focused commits and `CHANGELOG.md` records changes; there are no tagged releases or documented data-to-run provenance conventions. |
| 3 | Open collaboration | 3 / 10 | Contributors are credited, but there is no `CONTRIBUTING`, code of conduct, issue template, review policy, or maintainership information. |
| 4 | Reproducible environments | 5 / 10 | Module and backend settings are explicit in `form.yml.erb` and `template/sprocket.toml.erb`; there is no dependency lockfile or end-to-end setup procedure. |
| 5 | Data and workflow provenance | 3 / 10 | The launcher accepts workflow/input paths and uses scratch storage, but inputs, outputs, schemas, data sources, retention, and generated-artifact provenance are not documented. |
| 6 | Testing and validation | 2 / 10 | No test files, validation fixtures, test commands, or documented reproducibility checks are present. |
| 7 | Automation and continuous integration | 0 / 10 | No `.github/workflows` CI configuration or equivalent visible quality automation is present. |
| 8 | Documentation and usability | 6 / 10 | A README, changelog, and license exist and limitations are stated, but installation, configuration, usage, troubleshooting, and onboarding instructions are incomplete. |
| 9 | Licensing, attribution, and responsible reuse | 6 / 10 | An explicit `LICENSE` is present and contributors are named, but reuse, third-party attribution, release artifacts, and citation instructions are not explained. |
| 10 | Ethics, accessibility, and sustainability | 5 / 10 | The README states the LSF/HPC limitation and lack of guarantees, but no privacy or ethics considerations, accessibility practices, support channel, maintenance plan, or archival plan are documented. |
| **Total** |  | **49 / 100** | **Readiness snapshot; not an official certification.** |

## Evidence

Repository evidence is pinned to revision `efcaaf3f17794e304cd1139d84c9b43a1600d06a`:

- [README.md](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_WDL/blob/efcaaf3f17794e304cd1139d84c9b43a1600d06a/README.md)
- [CHANGELOG.md](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_WDL/blob/efcaaf3f17794e304cd1139d84c9b43a1600d06a/CHANGELOG.md)
- [form.yml.erb](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_WDL/blob/efcaaf3f17794e304cd1139d84c9b43a1600d06a/form.yml.erb)
- [template/script.sh.erb](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_WDL/blob/efcaaf3f17794e304cd1139d84c9b43a1600d06a/template/script.sh.erb)
- [template/sprocket.toml.erb](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_WDL/blob/efcaaf3f17794e304cd1139d84c9b43a1600d06a/template/sprocket.toml.erb)
- [LICENSE](https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_WDL/blob/efcaaf3f17794e304cd1139d84c9b43a1600d06a/LICENSE)

Turing Way evidence was retrieved from the project-design, project-documentation, and version-control guidance in the pinned `the-turing-way` resources. The evidence supports the criterion scores above; no points were awarded for practices that were not observable in the reviewed repository.

## Blocker

The globally requested `turing-way-certified` skill was not available in this runtime. The configured Turing Way MyGPT evidence and validation tools were available and used instead. No repository implementation blocker prevented creation of the requested artifacts.
