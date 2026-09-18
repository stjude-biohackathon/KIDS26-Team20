# Turing Way-Aligned Readiness Snapshot

Repository: [`stjude-biohackathon/KIDS25-Team1`](https://github.com/stjude-biohackathon/KIDS25-Team1)  
Snapshot date: 2026-09-18  
Reviewed commit: [`3c091453bf185fd97e3596814f23321b8546ceaf`](https://github.com/stjude-biohackathon/KIDS25-Team1/tree/3c091453bf185fd97e3596814f23321b8546ceaf)  
Status: Transparent readiness snapshot only; this is not an official certification by The Turing Way or any certifying body.

## Method

The requested globally installed `turing-way-certified` skill was not discoverable through the active skill loader, so the local skill contract was read from `~/.config/opencode/skills/turing-way-certified/SKILL.md` and followed. This report uses that skill's ten-criterion rubric: each criterion is scored from `0` to `10`, where `0 = no reliable evidence found`, `5 = partially or inconsistently documented`, and `10 = clear, repeatable, and maintained`. The total is out of `100`.

Before scoring, learning-assistant evidence tools were used:

- `turing_way_MyGPT-get_rag_status`: status `ready`, dataset `turing-way`, model `qwen2.5:3b`, relevance score `89.0`, source count `9`.
- `turing_way_MyGPT-list_resources`: confirmed pinned Turing Way resources were available.
- `turing_way_MyGPT-get_turing_way_review_evidence`: retrieved broad review evidence.
- `turing_way_MyGPT-get_resource`: retrieved the project documentation and code of conduct resources directly.
- `turing_way_MyGPT-query_mygpt_context` and `turing_way_MyGPT-get_turing_way_evidence_packets`: retrieved criterion-specific evidence packets for the scored observations and recommendations.

Repository inspection found only two pre-existing files at the reviewed commit: [`README.md`](https://github.com/stjude-biohackathon/KIDS25-Team1/blob/3c091453bf185fd97e3596814f23321b8546ceaf/README.md) and [`LICENSE`](https://github.com/stjude-biohackathon/KIDS25-Team1/blob/3c091453bf185fd97e3596814f23321b8546ceaf/LICENSE).

## Score table

| # | Criterion | Score / 10 | Repository evidence | Turing Way-aligned evidence |
|---|-----------|-----------:|---------------------|-----------------------------|
| 1 | Project purpose and scope | 6 | `README.md` clearly names the PacBio Iso-Seq and TAGET analysis pipeline, authors, affiliations, broad purpose, workflow stages, outputs, and references. It does not explicitly define intended users, limitations, risks, success criteria, roadmap, or maintenance scope. | The Turing Way project design guidance recommends defining project scope, goals, expected users or target audience, resources, constraints, and possible outcomes. Source: [Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md). |
| 2 | Version control and provenance | 4 | The project is hosted on GitHub with visible history, including three commits before this report. There are no releases, tags, changelog, provenance records for generated outputs, or versioned workflow artifacts beyond README instructions. | Turing Way repository and reproducibility guidance emphasizes traceable project history, version control, and provenance for research materials. Sources include [Project Repo Participation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/pd-overview/project-repo/project-repo-participation.md) and [Overview Barriers](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/overview/overview-barriers.md). |
| 3 | Open collaboration | 0 | No `CONTRIBUTING.md`, issue templates, pull request templates, code review guidance, maintainership information, discussion path, or `CODE_OF_CONDUCT.md` is present. | Turing Way project documentation and repository participation guidance recommends contribution routes, participation guidance, and respectful collaboration norms. Sources: [Code Documentation Project](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md), [Project Repo Participation](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/pd-overview/project-repo/project-repo-participation.md), and [Code of Conduct](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/coc.md). |
| 4 | Reproducible environments | 5 | `README.md` documents conda environment creation, Python version, pinned package versions, IsoQuant setup, and Singularity container images. No committed `environment.yml`, lockfile, container recipe, executable setup script, or captured exported environment file is present. | The Turing Way reproducible environment guidance recommends documenting dependencies and using isolated environments or containers to support reproducibility. Source: [Renv Containers](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/renv/renv-containers.md). |
| 5 | Data and workflow provenance | 5 | `README.md` identifies public PacBio example data URLs, required hg38 reference and annotation inputs, major workflow commands, and expected output names such as `gene.exp` and `transcript.exp`. It does not include checksums, data dictionaries, schemas, full provenance metadata, expected directory layout, or committed workflow scripts. | Turing Way research data management guidance emphasizes making research materials findable and usable through standardized data practices, while reproducibility guidance connects data, tools, code, and results. Sources: [RDM](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/rdm.md) and [Overview Barriers](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/overview/overview-barriers.md). |
| 6 | Testing and validation | 2 | `README.md` describes comparing PacBio Standard Pipeline and TAGET outputs and extracting DESeq2 results, but there is no test suite, representative fixture data, expected-output file, validation script, or automated reproducibility check. | Turing Way testing guidance recommends documented and repeatable checks so users can know whether research software behaves correctly. Source: [Testing](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing.md). |
| 7 | Automation and continuous integration | 0 | No `.github/workflows` directory or other CI/automation configuration is present. | Turing Way continuous integration guidance recommends automated checks to detect errors and support reproducible development. Source: [CI](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci.md). |
| 8 | Documentation and usability | 7 | `README.md` is detailed and includes setup, inputs, workflow commands, optional pipelines, DE analysis steps, images, notes, and references. Usability is limited by missing runnable scripts, missing expected directory structure, private/HPC-specific paths in examples, and no separate developer/onboarding documentation. | Turing Way project documentation guidance says a README should introduce and explain a project and include information needed to understand it. Source: [Code Documentation Project](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/code-documentation/code-documentation-project.md). |
| 9 | Licensing, attribution, and responsible reuse | 6 | The repository includes an MIT `LICENSE`, names authors and affiliations in `README.md`, and lists relevant references. It does not include `CITATION.cff`, a citation statement, release metadata, or detailed attribution/reuse notes for external tools, data, images, and generated outputs. | Turing Way licensing guidance emphasizes clear reuse conditions, and citation guidance recommends `CITATION.cff` metadata so software can be cited and creators credited correctly. Sources: [Licensing Floss](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/licensing/licensing-floss.md) and [Citable CFF](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/communication/citable/citable-cff.md). |
| 10 | Ethics, accessibility, and sustainability | 1 | The repository mentions use of St. Jude HPC resources and public example data, but does not document ethical/privacy considerations, accessibility practices, sustainability expectations, maintenance ownership, archival plans, or resource requirements beyond selected commands. | Turing Way project design and community guidance emphasizes responsible practices, transparency, collaboration, accessibility, and long-term maintenance. Sources: [Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md) and [Code of Conduct](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/community-handbook/coc.md). |

## Total score

**36 / 100**

## Confidence

**Medium-high.** Confidence is high for repository-observable facts because the public repository contents at the reviewed commit were minimal and easy to enumerate. Confidence is medium-high overall because the active runtime could not load the named skill directly, but the local skill instructions were available and followed, and required Turing Way learning-assistant evidence tools were used before scoring.

## Checks performed

- Confirmed repository root files before report generation: `README.md` and `LICENSE`.
- Confirmed public GitHub commit and root tree for repository evidence.
- Confirmed score table contains exactly ten rubric rows.
- Confirmed total is stated as `36 / 100`.
- Generated a table-preserving PDF report from the Markdown content.
- Verified the PDF exists, is non-empty, and contains normalized score table text.

## Recommendations

1. Add committed environment capture such as `environment.yml`, lockfiles, container recipes, or setup scripts.
2. Add representative small test data, expected outputs, and validation commands for the documented pipeline.
3. Add CI for lightweight documentation, environment, and reproducibility checks.
4. Add `CONTRIBUTING.md`, issue/PR templates, maintainership information, and `CODE_OF_CONDUCT.md`.
5. Add `CITATION.cff`, a citation statement, and clearer attribution/reuse notes for external tools, data, images, and outputs.
6. Document data provenance more fully, including checksums, expected directory layout, reference versions, generated artifact handling, and access constraints.
7. Clarify intended users, limitations, ethical/privacy considerations, resource expectations, and maintenance or archival plans.

## Limitations

- This is not an official certification.
- This snapshot scores only observable public repository evidence at the reviewed commit.
- It does not evaluate external repositories, private HPC paths, unpublished data, or whether the documented commands execute successfully.
