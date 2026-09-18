# Turing Way-Aligned Readiness Snapshot

> **This is not an official certification.** The Turing Way is public
> best-practice guidance for reproducible, ethical, and collaborative
> research, not a certifying authority. This document is a transparent,
> point-in-time readiness snapshot produced by scoring observable evidence in
> the repository against a ten-criterion rubric informed by Turing Way
> guidance. It carries no institutional, legal, or regulatory standing.

- **Repository reviewed:** [`stjude-biohackathon/KIDS25-Team22`](https://github.com/stjude-biohackathon/KIDS25-Team22)
- **Commit reviewed:** `403cd6324be70e30811f399fc556ca57bedbe189` (branch `main`)
- **Review date:** 2026-09-18
- **Scope:** Entire public repository as checked out at the commit above —
  README, LICENSE, source files (`main.py`, `agents.py`, `ranking.py`,
  `utils.py`, `llm_utils.py`, `Evo2score.py`, `config.py`, `prompts.py`),
  `app/` (Flask UI), `data/` (example/generated artifacts), Git history,
  GitHub issues/releases metadata (read via `gh`), and absence/presence of
  `.github/` automation, tests, and community-health files.
- **Confidence:** Medium. Findings are based on direct inspection of the
  repository's file tree, Git history, and public GitHub metadata (issues,
  license detection, visibility). No claims were accepted without a directly
  observed repository fact and its GitHub URL.

## Ten-criterion scoring (0–10 each, total out of 100)

| # | Criterion | Score /10 | Key observed evidence |
|---|-----------|:---:|---|
| 1 | Project purpose and scope | 5 | README states purpose ("Genesis: Multi-Modal Agentic AI for Cancer Variant Effect Prioritization") and audience, but has no dedicated "Scope" or "Known limitations" section beyond a brief "Notes, caveats" note. |
| 2 | Version control and provenance | 4 | 18 descriptive commits on `main`; no tags or GitHub releases exist (`git tag`, `gh release list` both empty), so there is no versioned/pinned snapshot of the code itself. |
| 3 | Open collaboration | 2 | GitHub Issues are enabled and used once (1 closed issue, #4), but there is no `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, PR template, or maintainership documentation. |
| 4 | Reproducible environments | 5 | `requirements.txt` pins exact versions (e.g. `Flask==3.1.2`, `ollama==0.5.4`) and README gives `conda create` / `pip install` steps, but there is no Dockerfile, `environment.yml`, or lockfile, and required API keys/internal endpoints (`ALPGENOME_API_KEY`, `PCAI_EVO2_ENDPOINT/TOKEN`) are named but not documented as to how to obtain or mock. |
| 5 | Data and workflow provenance | 3 | `data/` contains example/generated VCFs, a pickle object, and generated PDF/HTML reports, but there is no data dictionary, schema, or note documenting their source, generation date, or license terms. |
| 6 | Testing and validation | 0 | No automated test files, test framework, or documented steps to validate/reproduce pipeline outputs were found anywhere in the repository. |
| 7 | Automation and continuous integration | 0 | No `.github/workflows` directory or other CI configuration exists; nothing is automatically checked on push or pull request. |
| 8 | Documentation and usability | 6 | README.md (87 lines) is a fairly thorough onboarding guide with setup, CLI usage, web-UI usage, and a project-structure map, but lacks a deeper architecture/developer section describing how modules interact. |
| 9 | Licensing, attribution, and responsible reuse | 6 | A standard MIT `LICENSE` file is present with a clear copyright holder, and GitHub detects it as `mit`, but there is no `CITATION.cff` and no explicit attribution for third-party data (e.g. ClinVar) or model dependencies. |
| 10 | Ethics, accessibility, and sustainability | 1 | The project processes clinical/genomic variant data and depends on internal St. Jude infrastructure (per `config.py`/`main.py`/README), with no ethics, privacy, accessibility, or maintenance/sustainability statement anywhere in the repository. |

### **Total: 32 / 100**

## Evidence and citations

Each recommendation below pairs one directly observed repository fact (with
its public GitHub URL, pinned to the reviewed commit) with one pinned Turing
Way guidance citation retrieved via the required evidence tools.

| Area | Repository fact (evidence) | Recommendation | Turing Way citation |
|---|---|---|---|
| Purpose & scope | [README.md](https://github.com/stjude-biohackathon/KIDS25-Team22/blob/403cd6324be70e30811f399fc556ca57bedbe189/README.md) has no "Scope"/"Limitations" heading | Add a brief "Scope and limitations" section naming intended users, out-of-scope use cases, and known assumptions (e.g. St. Jude-internal endpoints). | [Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md) |
| Version control | No tags/releases at [commit 403cd63](https://github.com/stjude-biohackathon/KIDS25-Team22/commit/403cd6324be70e30811f399fc556ca57bedbe189) | Tag a release (e.g. `v0.1.0`) once the pipeline stabilizes so users can pin to a reproducible version. | [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md) |
| Open collaboration | No `CONTRIBUTING.md`/`CODE_OF_CONDUCT.md` at [repo root](https://github.com/stjude-biohackathon/KIDS25-Team22/tree/403cd6324be70e30811f399fc556ca57bedbe189) | Add a `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` describing how to file issues/PRs and review expectations. | [Contributing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/contributing.md) |
| Reproducible environments | [requirements.txt](https://github.com/stjude-biohackathon/KIDS25-Team22/blob/403cd6324be70e30811f399fc556ca57bedbe189/requirements.txt) pinned but no Dockerfile/lockfile | Provide a Dockerfile or `environment.yml`, and document how to obtain/mock required API keys and endpoints. | [Reproducibility Barriers](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/overview/overview-barriers.md) |
| Data provenance | [data/](https://github.com/stjude-biohackathon/KIDS25-Team22/tree/403cd6324be70e30811f399fc556ca57bedbe189/data) has no metadata/README | Add a short `data/README.md` documenting source, generation date, and license terms of bundled VCFs/reports. | [RDM Checklist](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm/rdm-checklist.md) |
| Testing | No test files found; see [README.md](https://github.com/stjude-biohackathon/KIDS25-Team22/blob/403cd6324be70e30811f399fc556ca57bedbe189/README.md) | Add at least a minimal `pytest` suite covering `ranking.py`/`utils.py`, and document how to run it. | [Testing Guidance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-guidance.md) |
| CI/automation | No `.github/workflows` at [repo root](https://github.com/stjude-biohackathon/KIDS25-Team22/tree/403cd6324be70e30811f399fc556ca57bedbe189) | Add a GitHub Actions workflow that at minimum lints/imports the Python modules on push/PR. | [CI Practices](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci/ci-practices.md) |
| Documentation | [README.md](https://github.com/stjude-biohackathon/KIDS25-Team22/blob/403cd6324be70e30811f399fc556ca57bedbe189/README.md) lists modules by name only | Expand README with a short architecture section describing how `agents.py`, `main.py`, and `app/app.py` interact. | [Code Documentation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md) |
| Licensing | [LICENSE](https://github.com/stjude-biohackathon/KIDS25-Team22/blob/403cd6324be70e30811f399fc556ca57bedbe189/LICENSE) present, no CITATION.cff | Add a `CITATION.cff` and note attribution for ClinVar and any third-party model/data dependencies. | [License](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/LICENSE.md) |
| Ethics/sustainability | [config.py](https://github.com/stjude-biohackathon/KIDS25-Team22/blob/403cd6324be70e30811f399fc556ca57bedbe189/config.py) references internal infra, no ethics note anywhere | Add a brief ethics/data-privacy note for clinical/genomic data use and a short post-hackathon maintenance plan. | [OSS Sustainability Challenges](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/collaboration/oss-sustainability/oss-sustainability-challenges.md) |

## Checks performed

- Cloned/inspected the repository worktree at commit `403cd63` (`git log`,
  `git tag`, file tree walk).
- Queried GitHub for issues, releases, license detection, and visibility via
  `gh repo view` / `gh issue list` / `gh release list`.
- Searched the full tree for test files, `.github/workflows`, `CONTRIBUTING`,
  `CODE_OF_CONDUCT`, `.gitignore`, `CITATION`, and data documentation.
- Read `README.md`, `LICENSE`, `requirements.txt`, `config.py`, and `main.py`
  in full.
- Retrieved Turing Way guidance via the required evidence tools
  (`get_turing_way_review_evidence`, `list_resources`, `get_resource`,
  `get_turing_way_evidence_packets`) before scoring, and paired every
  recommendation with a pinned citation and an observed repository fact.

## Limitations of this snapshot

- This review only inspected what is publicly visible in the Git repository
  and GitHub metadata; it did not attempt to run the pipeline, install
  dependencies, or verify runtime behavior of the Flask app or agent
  orchestration.
- No PHI or credentials were inspected or included; only public code and
  documentation were reviewed.
- Scores reflect a snapshot of commit `403cd63` and will change as the
  repository evolves.
- This snapshot does not evaluate scientific validity of the variant-ranking
  methodology, only reproducibility/collaboration/documentation practices.

## Final statement

**Total score: 32 / 100.** This is a Turing Way-aligned readiness snapshot,
not an official Turing Way certification, and not a security, clinical, or
institutional approval of any kind.
