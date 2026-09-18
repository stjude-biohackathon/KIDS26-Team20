const reportProjects = [
  {
    "name": "KIDS25 Team1",
    "cohort": "KIDS25 Hackathon",
    "score": 36,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team1 public hackathon repository, based on observable evidence.",
    "tags": [
      "Documentation",
      "Licensing",
      "Project design"
    ],
    "signals": [
      [
        "Project design",
        60,
        "Purpose and scope: 6 / 10"
      ],
      [
        "Reproducibility",
        50,
        "Environment + data provenance: 10 / 20"
      ],
      [
        "Validation",
        20,
        "Testing evidence: 2 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add committed environment capture such as environment.yml, lockfiles, container recipes, or setup scripts.",
      "Add representative small test data, expected outputs, and validation commands for the documented pipeline.",
      "Add CI for lightweight documentation, environment, and reproducibility checks."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team1/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team1/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team1"
  },
  {
    "name": "KIDS25 Team2",
    "cohort": "KIDS25 Hackathon",
    "score": 9,
    "status": "Foundational",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team2 public hackathon repository, based on observable evidence.",
    "tags": [
      "Licensing",
      "Provenance",
      "Automation"
    ],
    "signals": [
      [
        "Project design",
        0,
        "Purpose and scope: 0 / 10"
      ],
      [
        "Reproducibility",
        0,
        "Environment + data provenance: 0 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add a project purpose/scope section (research question, intended users, known limitations).",
      "Establish a real, incremental commit history with descriptive messages, and tag releases where appropriate.",
      "Add contribution guidance, a code of conduct, and maintainership information."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team2/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team2/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team2"
  },
  {
    "name": "KIDS25 Team3",
    "cohort": "KIDS25 Hackathon",
    "score": 25,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team3 public hackathon repository, based on observable evidence.",
    "tags": [
      "Provenance",
      "Licensing",
      "Project design"
    ],
    "signals": [
      [
        "Project design",
        30,
        "Purpose and scope: 3 / 10"
      ],
      [
        "Reproducibility",
        25,
        "Environment + data provenance: 5 / 20"
      ],
      [
        "Validation",
        10,
        "Testing evidence: 1 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add a project scope/purpose section. Expand README.md with the research question, intended users, and known limitations, following Project Design. Evidence: README.md is a one-line title with a script pipeline only.",
      "Tag stable releases. Use annotated Git tags/GitHub releases at meaningful milestones per Version Control. Evidence: history has 52 commits with PR merges but git tag is empty (commit history).",
      "Publish contribution and conduct guidance. Add CONTRIBUTING.md, CODEOFCONDUCT.md, and issue/PR templates, following Collaboration. Evidence: no such files exist in the tree (README.md as the closest onboarding doc)."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team3/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team3/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team3"
  },
  {
    "name": "KIDS25 Team4",
    "cohort": "KIDS25 Hackathon",
    "score": 33,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team4 public hackathon repository, based on observable evidence.",
    "tags": [
      "Documentation",
      "Project design",
      "Licensing"
    ],
    "signals": [
      [
        "Project design",
        60,
        "Purpose and scope: 6 / 10"
      ],
      [
        "Reproducibility",
        35,
        "Environment + data provenance: 7 / 20"
      ],
      [
        "Validation",
        10,
        "Testing evidence: 1 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add a .github/workflows/ CI pipeline (lint + a smoke test) — highest-impact gap (Criteria 6 & 7 currently score 0–1).",
      "Add CONTRIBUTING.md and CODEOFCONDUCT.md to enable structured open collaboration (Criterion 3).",
      "Consolidate environment files into one pinned, documented environment (or the already-planned Docker/Singularity container) at the repo root (Criterion 4)."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team4/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team4/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team4"
  },
  {
    "name": "KIDS25 Team5",
    "cohort": "KIDS25 Hackathon",
    "score": 27,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team5 public hackathon repository, based on observable evidence.",
    "tags": [
      "Data provenance",
      "Documentation",
      "Licensing"
    ],
    "signals": [
      [
        "Project design",
        30,
        "Purpose and scope: 3 / 10"
      ],
      [
        "Reproducibility",
        35,
        "Environment + data provenance: 7 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Expand README.md to state the project's research question/purpose, intended users, scope, and known limitations, per The Turing Way's Guide for Project Design. Repository fact: README.md is currently a single line.",
      "Adopt Git LFS (or an equivalent) for large binary datasets to keep provenance traceable without bloating the main Git history, per The Turing Way's Version Control chapter. Repository fact: ~1.5GB of .sas7bdat files under sasdata/ are committed directly with no LFS configuration.",
      "Add CONTRIBUTING.md and CODEOFCONDUCT.md to formalize how outside contributors can engage, per The Turing Way's Contributing guidance. Repository fact: No CONTRIBUTING.md, CODEOFCONDUCT.md, or .github/ directory exists; 5 open issues track work informally."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team5/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team5/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team5"
  },
  {
    "name": "KIDS25 Team6",
    "cohort": "KIDS25 Hackathon",
    "score": 36,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team6 public hackathon repository, based on observable evidence.",
    "tags": [
      "Environments",
      "Provenance",
      "Data provenance"
    ],
    "signals": [
      [
        "Project design",
        50,
        "Purpose and scope: 5 / 10"
      ],
      [
        "Reproducibility",
        60,
        "Environment + data provenance: 12 / 20"
      ],
      [
        "Validation",
        20,
        "Testing evidence: 2 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Run tests and lightweight quality checks automatically on every pull request.",
      "Document privacy and ethical boundaries, accessibility, maintenance ownership, and archival plans.",
      "Add contribution guidance, community standards, issue templates, and clear maintainer ownership."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team6/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team6/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team6"
  },
  {
    "name": "KIDS25 Team7",
    "cohort": "KIDS25 Hackathon",
    "score": 26,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team7 public hackathon repository, based on observable evidence.",
    "tags": [
      "Provenance",
      "Licensing",
      "Environments"
    ],
    "signals": [
      [
        "Project design",
        20,
        "Purpose and scope: 2 / 10"
      ],
      [
        "Reproducibility",
        30,
        "Environment + data provenance: 6 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Write a real root README covering the project's purpose (a chemical compound registration/search tool built at the St. Jude BioHackathon), intended users, current scope, and known limitations. (Criterion 1 — Project Design)",
      "Tag a release (e.g. v0.1.0-hackathon) to create a citable, pinned snapshot of the working prototype. (Criterion 2 — Version Control)",
      "Add CONTRIBUTING.md and CODEOFCONDUCT.md describing how to propose changes, review expectations, and community conduct standards. (Criterion 3 — Collaboration)"
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team7/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team7/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team7"
  },
  {
    "name": "KIDS25 Team8 · cmdsaw",
    "cohort": "KIDS25 Hackathon",
    "score": 44,
    "status": "Progressing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team8 · cmdsaw public hackathon repository, based on observable evidence.",
    "tags": [
      "Documentation",
      "Data provenance",
      "Licensing"
    ],
    "signals": [
      [
        "Project design",
        60,
        "Purpose and scope: 6 / 10"
      ],
      [
        "Reproducibility",
        55,
        "Environment + data provenance: 11 / 20"
      ],
      [
        "Validation",
        60,
        "Testing evidence: 6 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Publish a roadmap and changelog. The README names a planned feature, but no roadmap or changelog is tracked. The Turing Way: Project Documentation identifies both as core project documentation.",
      "Make collaboration explicit. Add CONTRIBUTING.md, CODEOFCONDUCT.md, maintainer contacts, and concise review expectations. The repository currently only invites issues and pull requests. The Turing Way: Collaboration emphasizes contribution-friendly, inclusive collaboration and clear expectations.",
      "Make the software citable. Add CITATION.cff and archive a tagged release to establish persistent citation metadata; the current README citation is plain text only. The Turing Way: Project Documentation specifically recommends CITATION.cff."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team8_cmdsaw/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team8_cmdsaw/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team8_cmdsaw"
  },
  {
    "name": "KIDS25 Team8 · flowjomojo",
    "cohort": "KIDS25 Hackathon",
    "score": 37,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team8 · flowjomojo public hackathon repository, based on observable evidence.",
    "tags": [
      "Documentation",
      "Project design",
      "Licensing"
    ],
    "signals": [
      [
        "Project design",
        70,
        "Purpose and scope: 7 / 10"
      ],
      [
        "Reproducibility",
        45,
        "Environment + data provenance: 9 / 20"
      ],
      [
        "Validation",
        20,
        "Testing evidence: 2 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Run tests and lightweight quality checks automatically on every pull request.",
      "Document privacy and ethical boundaries, accessibility, maintenance ownership, and archival plans.",
      "Add contribution guidance, community standards, issue templates, and clear maintainer ownership."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team8_flowjomojo/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team8_flowjomojo/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team8_flowjomojo"
  },
  {
    "name": "KIDS25 Team8 · OnDemand Nextflow",
    "cohort": "KIDS25 Hackathon",
    "score": 28,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team8 · OnDemand Nextflow public hackathon repository, based on observable evidence.",
    "tags": [
      "Provenance",
      "Licensing",
      "Project design"
    ],
    "signals": [
      [
        "Project design",
        40,
        "Purpose and scope: 4 / 10"
      ],
      [
        "Reproducibility",
        35,
        "Environment + data provenance: 7 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add a deployment and user guide covering Open OnDemand/LSF prerequisites, supported versions, configuration, a minimal parameters example, expected outputs, and troubleshooting.",
      "Add template/configuration checks and a representative submission smoke test; execute them in pull-request CI.",
      "Publish CONTRIBUTING.md, CODEOFCONDUCT.md, maintainership/support details, and issue templates."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team8_OnDemand_Nextflow/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team8_OnDemand_Nextflow/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_Nextflow"
  },
  {
    "name": "KIDS25 Team8 · OnDemand WDL",
    "cohort": "KIDS25 Hackathon",
    "score": 43,
    "status": "Progressing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team8 · OnDemand WDL public hackathon repository, based on observable evidence.",
    "tags": [
      "Provenance",
      "Documentation",
      "Licensing"
    ],
    "signals": [
      [
        "Project design",
        60,
        "Purpose and scope: 6 / 10"
      ],
      [
        "Reproducibility",
        40,
        "Environment + data provenance: 8 / 20"
      ],
      [
        "Validation",
        20,
        "Testing evidence: 2 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Run tests and lightweight quality checks automatically on every pull request.",
      "Add deterministic tests with small fixtures and documented expected results.",
      "Document data sources, versions, checksums, schemas, transformations, and generated artifacts."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team8_OnDemand_WDL/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team8_OnDemand_WDL/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team8_OnDemand_WDL"
  },
  {
    "name": "KIDS25 Team9",
    "cohort": "KIDS25 Hackathon",
    "score": 22,
    "status": "Developing",
    "confidence": "Medium-high",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team9 public hackathon repository, based on observable evidence.",
    "tags": [
      "Licensing",
      "Project design",
      "Provenance"
    ],
    "signals": [
      [
        "Project design",
        40,
        "Purpose and scope: 4 / 10"
      ],
      [
        "Reproducibility",
        20,
        "Environment + data provenance: 4 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Run tests and lightweight quality checks automatically on every pull request.",
      "Document privacy and ethical boundaries, accessibility, maintenance ownership, and archival plans.",
      "Add deterministic tests with small fixtures and documented expected results."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team9/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team9/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team9"
  },
  {
    "name": "KIDS25 Team10",
    "cohort": "KIDS25 Hackathon",
    "score": 25,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team10 public hackathon repository, based on observable evidence.",
    "tags": [
      "Documentation",
      "Licensing",
      "Project design"
    ],
    "signals": [
      [
        "Project design",
        50,
        "Purpose and scope: 5 / 10"
      ],
      [
        "Reproducibility",
        20,
        "Environment + data provenance: 4 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add deterministic, portable tests and CI for the file-crawler and participant-finder R scripts, using small non-sensitive fixture directories, and run them automatically on every push/PR.",
      "Pin R dependencies and capture the environment (e.g., an renv.lock or DESCRIPTION file) instead of unversioned install.packages() calls.",
      "Add contributor and governance documentation — CONTRIBUTING.md, CODEOFCONDUCT.md, and issue/PR templates — to support open, reviewable collaboration."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team10/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team10/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team10"
  },
  {
    "name": "KIDS25 Team11",
    "cohort": "KIDS25 Hackathon",
    "score": 17,
    "status": "Foundational",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team11 public hackathon repository, based on observable evidence.",
    "tags": [
      "Licensing",
      "Project design",
      "Documentation"
    ],
    "signals": [
      [
        "Project design",
        40,
        "Purpose and scope: 4 / 10"
      ],
      [
        "Reproducibility",
        10,
        "Environment + data provenance: 2 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add automated tests and a CI workflow (criteria 6–7, currently 0/10 each). Even a minimal .github/workflows/ job that runs R CMD check or loads app.R/server.R/ui.R to catch syntax errors would substantially raise reproducibility confidence. See The Turing Way's Testing and CI guidance.",
      "Declare and pin dependencies (criterion 4, 1/10). Add an R DESCRIPTION file or renv.lock and README setup instructions so others can reproduce the Shiny app's environment. See Reproducible Research.",
      "Add open-collaboration documentation (criterion 3, 0/10): a CONTRIBUTING.md and CODEOFCONDUCT.md clarify how others can contribute and what conduct is expected. See Code of Conduct."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team11/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team11/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team11"
  },
  {
    "name": "KIDS25 Team12",
    "cohort": "KIDS25 Hackathon",
    "score": 24,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team12 public hackathon repository, based on observable evidence.",
    "tags": [
      "Provenance",
      "Environments",
      "Licensing"
    ],
    "signals": [
      [
        "Project design",
        10,
        "Purpose and scope: 1 / 10"
      ],
      [
        "Reproducibility",
        30,
        "Environment + data provenance: 6 / 20"
      ],
      [
        "Validation",
        10,
        "Testing evidence: 1 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add tests that exercise the declared vitest/@vue/test-utils tooling. The test script exists but nothing runs it against real code, so testing/validation is unverifiable. Turing Way guidance: Testing Guidance",
      "Add a CI workflow (e.g. GitHub Actions) to run linting, type-checking (vue-tsc), and tests automatically on push/PR, since none currently exists. Turing Way guidance: CI Practices",
      "Add CONTRIBUTING.md, CODEOFCONDUCT.md, and issue/PR templates. With 4 active contributors and no documented review process, contribution norms are currently implicit only. Turing Way guidance: Version Control"
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team12/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team12/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team12"
  },
  {
    "name": "KIDS25 Team13",
    "cohort": "KIDS25 Hackathon",
    "score": 8,
    "status": "Foundational",
    "confidence": "High",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team13 public hackathon repository, based on observable evidence.",
    "tags": [
      "Licensing",
      "Collaboration",
      "Provenance"
    ],
    "signals": [
      [
        "Project design",
        0,
        "Purpose and scope: 0 / 10"
      ],
      [
        "Reproducibility",
        0,
        "Environment + data provenance: 0 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Write a real README covering the project's research question, scope, intended users, and known limitations (cites Project Design).",
      "Merge or close the pending pull request and adopt an incremental commit and tagging/release practice going forward (cites Version Control).",
      "Add CONTRIBUTING.md, CODEOFCONDUCT.md, and issue/PR templates to set expectations for contributors (cites Maintaining and Reviewing Contributions)."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team13/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team13/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team13"
  },
  {
    "name": "KIDS25 Team14",
    "cohort": "KIDS25 Hackathon",
    "score": 32,
    "status": "Developing",
    "confidence": "Medium-high",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team14 public hackathon repository, based on observable evidence.",
    "tags": [
      "Project design",
      "Licensing",
      "Provenance"
    ],
    "signals": [
      [
        "Project design",
        60,
        "Purpose and scope: 6 / 10"
      ],
      [
        "Reproducibility",
        30,
        "Environment + data provenance: 6 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add a limitations/scope note to the README — state known limitations of the enrichment methods and target audience (Project Design guidance).",
      "Tag a release and adopt semantic versioning — even a single v0.1 tag would let others cite a stable snapshot (Version Control guidance).",
      "Add CONTRIBUTING.md and CODEOFCONDUCT.md — clarify how external contributors can propose changes and what conduct is expected (Contributing guidance)."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team14/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team14/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team14"
  },
  {
    "name": "KIDS25 Team15",
    "cohort": "KIDS25 Hackathon",
    "score": 28,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team15 public hackathon repository, based on observable evidence.",
    "tags": [
      "Project design",
      "Documentation",
      "Licensing"
    ],
    "signals": [
      [
        "Project design",
        60,
        "Purpose and scope: 6 / 10"
      ],
      [
        "Reproducibility",
        30,
        "Environment + data provenance: 6 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add automated tests and CI (criteria 6–7): introduce a minimal test suite (e.g. pytest for the FastAPI backend, a Vitest/Jest suite for judee-web) and a GitHub Actions workflow that runs them on every push and pull request.",
      "Document the scraped datasets (criterion 5): add a README.md (or data dictionary) inside backend/scrappeddata/ describing the source, collection date, scope, and schema of each CSV file.",
      "Add contribution and community-health files (criterion 3): add CONTRIBUTING.md and CODEOFCONDUCT.md, and consider .github/ISSUETEMPLATE files."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team15/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team15/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team15"
  },
  {
    "name": "KIDS25 Team16",
    "cohort": "KIDS25 Hackathon",
    "score": 9,
    "status": "Foundational",
    "confidence": "High",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team16 public hackathon repository, based on observable evidence.",
    "tags": [
      "Licensing",
      "Provenance",
      "Automation"
    ],
    "signals": [
      [
        "Project design",
        0,
        "Purpose and scope: 0 / 10"
      ],
      [
        "Reproducibility",
        0,
        "Environment + data provenance: 0 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add a real README — describe the project's purpose, research question, intended users, and known limitations (Criterion 1, 8). See Project Design and Code Documentation — Project Level.",
      "Add CONTRIBUTING.md and CODEOFCONDUCT.md to enable open collaboration and set review expectations (Criterion 3). See Contributing.",
      "Commit actual project code/data/workflows with descriptive, incremental commit messages rather than a single placeholder commit, and document data sources and workflow steps as they are added (Criterion 2, 5). See Version Control and RDM Checklist."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team16/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team16/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team16"
  },
  {
    "name": "KIDS25 Team17",
    "cohort": "KIDS25 Hackathon",
    "score": 28,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team17 public hackathon repository, based on observable evidence.",
    "tags": [
      "Documentation",
      "Licensing",
      "Project design"
    ],
    "signals": [
      [
        "Project design",
        40,
        "Purpose and scope: 4 / 10"
      ],
      [
        "Reproducibility",
        35,
        "Environment + data provenance: 7 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add automated tests and document how to run them.",
      "Add continuous integration to run checks automatically.",
      "Adopt clearer, incremental commit messages and tagged releases."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team17/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team17/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team17"
  },
  {
    "name": "KIDS25 Team18",
    "cohort": "KIDS25 Hackathon",
    "score": 16,
    "status": "Foundational",
    "confidence": "Medium-high",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team18 public hackathon repository, based on observable evidence.",
    "tags": [
      "Licensing",
      "Provenance",
      "Data provenance"
    ],
    "signals": [
      [
        "Project design",
        0,
        "Purpose and scope: 0 / 10"
      ],
      [
        "Reproducibility",
        20,
        "Environment + data provenance: 4 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Run tests and lightweight quality checks automatically on every pull request.",
      "Document privacy and ethical boundaries, accessibility, maintenance ownership, and archival plans.",
      "Add contribution guidance, community standards, issue templates, and clear maintainer ownership."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team18/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team18/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team18"
  },
  {
    "name": "KIDS25 Team19",
    "cohort": "KIDS25 Hackathon",
    "score": 11,
    "status": "Foundational",
    "confidence": "Medium-high",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team19 public hackathon repository, based on observable evidence.",
    "tags": [
      "Licensing",
      "Provenance",
      "Data provenance"
    ],
    "signals": [
      [
        "Project design",
        0,
        "Purpose and scope: 0 / 10"
      ],
      [
        "Reproducibility",
        10,
        "Environment + data provenance: 2 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Project purpose and scope: Add a README describing the app's purpose (SRM email templating for St. Jude Shared Resources), intended users, and known limitations, per Turing Way project design guidance.",
      "Version control and provenance: Adopt descriptive commit messages and tag releases as the app stabilizes.",
      "Open collaboration: Add CONTRIBUTING.md, a code of conduct, and clarify maintainership/issue-reporting paths."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team19/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team19/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team19"
  },
  {
    "name": "KIDS25 Team21",
    "cohort": "KIDS25 Hackathon",
    "score": 14,
    "status": "Foundational",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team21 public hackathon repository, based on observable evidence.",
    "tags": [
      "Provenance",
      "Licensing",
      "Documentation"
    ],
    "signals": [
      [
        "Project design",
        10,
        "Purpose and scope: 1 / 10"
      ],
      [
        "Reproducibility",
        15,
        "Environment + data provenance: 3 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Add a root-level README.md stating the project's purpose (a biohackathon lab-protocol knowledge base and chatbot), scope, intended users, and known limitations.",
      "Add CONTRIBUTING.md and CODEOFCONDUCT.md at the repository root to support open collaboration and set contributor expectations.",
      "Pin dependency versions in CODE/requirements.txt (or add a lockfile / environment.yml) and document the supported Python version."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team21/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team21/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team21"
  },
  {
    "name": "KIDS25 Team22",
    "cohort": "KIDS25 Hackathon",
    "score": 32,
    "status": "Developing",
    "confidence": "Moderate",
    "description": "A Turing Way-aligned readiness snapshot of the KIDS25 Team22 public hackathon repository, based on observable evidence.",
    "tags": [
      "Documentation",
      "Licensing",
      "Project design"
    ],
    "signals": [
      [
        "Project design",
        50,
        "Purpose and scope: 5 / 10"
      ],
      [
        "Reproducibility",
        40,
        "Environment + data provenance: 8 / 20"
      ],
      [
        "Validation",
        0,
        "Testing evidence: 0 / 10"
      ],
      [
        "Automation",
        0,
        "CI evidence: 0 / 10"
      ]
    ],
    "improvements": [
      "Run tests and lightweight quality checks automatically on every pull request.",
      "Add deterministic tests with small fixtures and documented expected results.",
      "Document privacy and ethical boundaries, accessibility, maintenance ownership, and archival plans."
    ],
    "reviewed": "2026-09-18",
    "reportPdf": "reports/KIDS25-Team22/TURING_WAY_CERTIFICATION.pdf",
    "reportMarkdown": "reports/KIDS25-Team22/TURING_WAY_CERTIFICATION.md",
    "repository": "https://github.com/stjude-biohackathon/KIDS25-Team22"
  }
];


const reportCriteria = {
  "KIDS25 Team1": [
    [
      "Project purpose and scope",
      6
    ],
    [
      "Version control and provenance",
      4
    ],
    [
      "Open collaboration",
      0
    ],
    [
      "Reproducible environments",
      5
    ],
    [
      "Data and workflow provenance",
      5
    ],
    [
      "Testing and validation",
      2
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      7
    ],
    [
      "Licensing, attribution, and responsible reuse",
      6
    ],
    [
      "Ethics, accessibility, and sustainability",
      1
    ]
  ],
  "KIDS25 Team10": [
    [
      "Project purpose and scope",
      5
    ],
    [
      "Version control and provenance",
      2
    ],
    [
      "Open collaboration",
      1
    ],
    [
      "Reproducible environments",
      1
    ],
    [
      "Data and workflow provenance",
      3
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      6
    ],
    [
      "Licensing, attribution, and responsible reuse",
      6
    ],
    [
      "Ethics, accessibility, and sustainability",
      1
    ]
  ],
  "KIDS25 Team11": [
    [
      "Project purpose and scope",
      4
    ],
    [
      "Version control and provenance",
      2
    ],
    [
      "Open collaboration",
      0
    ],
    [
      "Reproducible environments",
      1
    ],
    [
      "Data and workflow provenance",
      1
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      3
    ],
    [
      "Licensing, attribution, and responsible reuse",
      6
    ],
    [
      "Ethics, accessibility, and sustainability",
      0
    ]
  ],
  "KIDS25 Team12": [
    [
      "Project purpose and scope",
      1
    ],
    [
      "Version control and provenance",
      6
    ],
    [
      "Open collaboration",
      2
    ],
    [
      "Reproducible environments",
      5
    ],
    [
      "Data and workflow provenance",
      1
    ],
    [
      "Testing and validation",
      1
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      3
    ],
    [
      "Licensing, attribution, and responsible reuse",
      4
    ],
    [
      "Ethics, accessibility, and sustainability",
      1
    ]
  ],
  "KIDS25 Team13": [
    [
      "Project purpose and scope",
      0
    ],
    [
      "Version control and provenance",
      1
    ],
    [
      "Open collaboration",
      1
    ],
    [
      "Reproducible environments",
      0
    ],
    [
      "Data and workflow provenance",
      0
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      0
    ],
    [
      "Licensing, attribution, and responsible reuse",
      6
    ],
    [
      "Ethics, accessibility, and sustainability",
      0
    ]
  ],
  "KIDS25 Team14": [
    [
      "Project purpose and scope",
      6
    ],
    [
      "Version control and provenance",
      5
    ],
    [
      "Open collaboration",
      3
    ],
    [
      "Reproducible environments",
      2
    ],
    [
      "Data and workflow provenance",
      4
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      4
    ],
    [
      "Licensing, attribution, and responsible reuse",
      5
    ],
    [
      "Ethics, accessibility, and sustainability",
      3
    ]
  ],
  "KIDS25 Team15": [
    [
      "Project purpose and scope",
      6
    ],
    [
      "Version control and provenance",
      5
    ],
    [
      "Open collaboration",
      1
    ],
    [
      "Reproducible environments",
      5
    ],
    [
      "Data and workflow provenance",
      1
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      5
    ],
    [
      "Licensing, attribution, and responsible reuse",
      5
    ],
    [
      "Ethics, accessibility, and sustainability",
      0
    ]
  ],
  "KIDS25 Team16": [
    [
      "Project purpose and scope",
      0
    ],
    [
      "Version control and provenance",
      1
    ],
    [
      "Open collaboration",
      0
    ],
    [
      "Reproducible environments",
      0
    ],
    [
      "Data and workflow provenance",
      0
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      0
    ],
    [
      "Licensing, attribution, and responsible reuse",
      8
    ],
    [
      "Ethics, accessibility, and sustainability",
      0
    ]
  ],
  "KIDS25 Team17": [
    [
      "Project purpose and scope",
      4
    ],
    [
      "Version control and provenance",
      4
    ],
    [
      "Open collaboration",
      2
    ],
    [
      "Reproducible environments",
      4
    ],
    [
      "Data and workflow provenance",
      3
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      5
    ],
    [
      "Licensing, attribution, and responsible reuse",
      5
    ],
    [
      "Ethics, accessibility, and sustainability",
      1
    ]
  ],
  "KIDS25 Team18": [
    [
      "Project purpose and scope",
      0
    ],
    [
      "Version control and provenance",
      4
    ],
    [
      "Open collaboration",
      0
    ],
    [
      "Reproducible environments",
      2
    ],
    [
      "Data and workflow provenance",
      2
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      2
    ],
    [
      "Licensing, attribution, and responsible reuse",
      6
    ],
    [
      "Ethics, accessibility, and sustainability",
      0
    ]
  ],
  "KIDS25 Team19": [
    [
      "Project purpose and scope",
      0
    ],
    [
      "Version control and provenance",
      2
    ],
    [
      "Open collaboration",
      0
    ],
    [
      "Reproducible environments",
      1
    ],
    [
      "Data and workflow provenance",
      1
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      1
    ],
    [
      "Licensing, attribution, and responsible reuse",
      6
    ],
    [
      "Ethics, accessibility, and sustainability",
      0
    ]
  ],
  "KIDS25 Team2": [
    [
      "Project purpose and scope",
      0
    ],
    [
      "Version control and provenance",
      1
    ],
    [
      "Open collaboration",
      0
    ],
    [
      "Reproducible environments",
      0
    ],
    [
      "Data and workflow provenance",
      0
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      0
    ],
    [
      "Licensing, attribution, and responsible reuse",
      8
    ],
    [
      "Ethics, accessibility, and sustainability",
      0
    ]
  ],
  "KIDS25 Team21": [
    [
      "Project purpose and scope",
      1
    ],
    [
      "Version control and provenance",
      4
    ],
    [
      "Open collaboration",
      1
    ],
    [
      "Reproducible environments",
      2
    ],
    [
      "Data and workflow provenance",
      1
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      2
    ],
    [
      "Licensing, attribution, and responsible reuse",
      3
    ],
    [
      "Ethics, accessibility, and sustainability",
      0
    ]
  ],
  "KIDS25 Team22": [
    [
      "Project purpose and scope",
      5
    ],
    [
      "Version control and provenance",
      4
    ],
    [
      "Open collaboration",
      2
    ],
    [
      "Reproducible environments",
      5
    ],
    [
      "Data and workflow provenance",
      3
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      6
    ],
    [
      "Licensing, attribution, and responsible reuse",
      6
    ],
    [
      "Ethics, accessibility, and sustainability",
      1
    ]
  ],
  "KIDS25 Team3": [
    [
      "Project purpose and scope",
      3
    ],
    [
      "Version control and provenance",
      6
    ],
    [
      "Open collaboration",
      2
    ],
    [
      "Reproducible environments",
      3
    ],
    [
      "Data and workflow provenance",
      2
    ],
    [
      "Testing and validation",
      1
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      2
    ],
    [
      "Licensing, attribution, and responsible reuse",
      5
    ],
    [
      "Ethics, accessibility, and sustainability",
      1
    ]
  ],
  "KIDS25 Team4": [
    [
      "Project purpose and scope",
      6
    ],
    [
      "Version control and provenance",
      5
    ],
    [
      "Open collaboration",
      2
    ],
    [
      "Reproducible environments",
      4
    ],
    [
      "Data and workflow provenance",
      3
    ],
    [
      "Testing and validation",
      1
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      6
    ],
    [
      "Licensing, attribution, and responsible reuse",
      5
    ],
    [
      "Ethics, accessibility, and sustainability",
      1
    ]
  ],
  "KIDS25 Team5": [
    [
      "Project purpose and scope",
      3
    ],
    [
      "Version control and provenance",
      4
    ],
    [
      "Open collaboration",
      3
    ],
    [
      "Reproducible environments",
      1
    ],
    [
      "Data and workflow provenance",
      6
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      5
    ],
    [
      "Licensing, attribution, and responsible reuse",
      4
    ],
    [
      "Ethics, accessibility, and sustainability",
      1
    ]
  ],
  "KIDS25 Team6": [
    [
      "Project purpose and scope",
      5
    ],
    [
      "Version control and provenance",
      6
    ],
    [
      "Open collaboration",
      1
    ],
    [
      "Reproducible environments",
      7
    ],
    [
      "Data and workflow provenance",
      5
    ],
    [
      "Testing and validation",
      2
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      5
    ],
    [
      "Licensing, attribution, and responsible reuse",
      4
    ],
    [
      "Ethics, accessibility, and sustainability",
      1
    ]
  ],
  "KIDS25 Team7": [
    [
      "Project purpose and scope",
      2
    ],
    [
      "Version control and provenance",
      6
    ],
    [
      "Open collaboration",
      3
    ],
    [
      "Reproducible environments",
      5
    ],
    [
      "Data and workflow provenance",
      1
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      4
    ],
    [
      "Licensing, attribution, and responsible reuse",
      5
    ],
    [
      "Ethics, accessibility, and sustainability",
      0
    ]
  ],
  "KIDS25 Team8 · OnDemand Nextflow": [
    [
      "Project purpose and scope",
      4
    ],
    [
      "Version control and provenance",
      7
    ],
    [
      "Open collaboration",
      1
    ],
    [
      "Reproducible environments",
      4
    ],
    [
      "Data and workflow provenance",
      3
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      3
    ],
    [
      "Licensing, attribution, and responsible reuse",
      5
    ],
    [
      "Ethics, accessibility, and sustainability",
      1
    ]
  ],
  "KIDS25 Team8 · OnDemand WDL": [
    [
      "Project purpose and scope",
      6
    ],
    [
      "Version control and provenance",
      7
    ],
    [
      "Open collaboration",
      3
    ],
    [
      "Reproducible environments",
      5
    ],
    [
      "Data and workflow provenance",
      3
    ],
    [
      "Testing and validation",
      2
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      6
    ],
    [
      "Licensing, attribution, and responsible reuse",
      6
    ],
    [
      "Ethics, accessibility, and sustainability",
      5
    ]
  ],
  "KIDS25 Team8 · cmdsaw": [
    [
      "Project purpose and scope",
      6
    ],
    [
      "Version control and provenance",
      5
    ],
    [
      "Open collaboration",
      2
    ],
    [
      "Reproducible environments",
      5
    ],
    [
      "Data and workflow provenance",
      6
    ],
    [
      "Testing and validation",
      6
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      7
    ],
    [
      "Licensing, attribution, and responsible reuse",
      6
    ],
    [
      "Ethics, accessibility, and sustainability",
      1
    ]
  ],
  "KIDS25 Team8 · flowjomojo": [
    [
      "Project purpose and scope",
      7
    ],
    [
      "Version control and provenance",
      5
    ],
    [
      "Open collaboration",
      1
    ],
    [
      "Reproducible environments",
      5
    ],
    [
      "Data and workflow provenance",
      4
    ],
    [
      "Testing and validation",
      2
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      7
    ],
    [
      "Licensing, attribution, and responsible reuse",
      6
    ],
    [
      "Ethics, accessibility, and sustainability",
      0
    ]
  ],
  "KIDS25 Team9": [
    [
      "Project purpose and scope",
      4
    ],
    [
      "Version control and provenance",
      4
    ],
    [
      "Open collaboration",
      3
    ],
    [
      "Reproducible environments",
      2
    ],
    [
      "Data and workflow provenance",
      2
    ],
    [
      "Testing and validation",
      0
    ],
    [
      "Automation and continuous integration",
      0
    ],
    [
      "Documentation and usability",
      3
    ],
    [
      "Licensing, attribution, and responsible reuse",
      4
    ],
    [
      "Ethics, accessibility, and sustainability",
      0
    ]
  ]
};
