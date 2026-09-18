# Turing Way-Aligned Readiness Snapshot

> **This is not an official certification.** The Turing Way is public
> best-practice guidance for reproducible, collaborative, and open research
> projects — it is not a certification authority, and no institution has
> authorized this document as a formal compliance certificate. This report is
> a transparent, evidence-based readiness snapshot only.

- **Repository:** stjude-biohackathon/KIDS25-Team12
- **Reviewed commit:** `8dafc2816e4f7aee61a5fcc486a2d34e63932f77` (`main`)
- **Review date:** 2026-09-18
- **Scope:** Full public repository as checked out (application source under
  `src/`, `public/`, `Image Projects/`, build/config files, `README.md`,
  `LICENSE`, and git history). No private or sensitive data was reviewed.
- **Confidence:** Medium. Findings are based on direct inspection of files,
  `git log`, and `package.json` in the working tree; no network access to the
  live GitHub UI (issues/discussions/branch protection) was used, so
  collaboration surfaces hosted only on GitHub.com could not be verified
  beyond what is committed to the repository.

## Ten-criterion rubric (0–10 each, total out of 100)

| # | Criterion | Score | Key evidence |
|---|-----------|:-----:|---------------|
| 1 | Project purpose and scope | 1/10 | `README.md` contains only "How to run" instructions and generic Vue 3 + TypeScript + Vite template boilerplate; no stated research question, purpose, intended users, or known limitations. |
| 2 | Version control and provenance | 6/10 | `git log` shows 47 commits from 4 named contributors with descriptive `feat:`/`fix:` messages and merge commits, giving a traceable history; however, no Git tags or releases exist to pin provenance of shipped versions. |
| 3 | Open collaboration | 2/10 | No `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, or `.github/ISSUE_TEMPLATE` files exist despite 4 active contributors, so contribution norms and review expectations are undocumented. |
| 4 | Reproducible environments | 5/10 | `README.md` documents `npm run dev` and pins exact `node`, `npm`, `vuetify`, and `vite` versions used; `package-lock.json` pins transitive dependencies. No containerization (e.g. Dockerfile) or OS/environment capture beyond Node tooling. |
| 5 | Data and workflow provenance | 1/10 | `public/` and `Image Projects/` contain many generated images and audio assets (e.g. `Generated Image September 30, 2025 - 2_26PM.png`) with no documentation of their source, generation workflow, or licensing/attribution. |
| 6 | Testing and validation | 1/10 | `package.json` declares a `test` script (`vitest`) and lists `vitest`/`@vue/test-utils` as devDependencies, but no `*.spec.ts` or `*.test.ts` files exist anywhere in the repository — the tooling is unused. |
| 7 | Automation and continuous integration | 0/10 | No `.github/workflows` directory or any other CI/automation configuration exists in the repository. |
| 8 | Documentation and usability | 3/10 | README covers only run steps and unedited Vue/Vite template text (IDE setup, `.vue` type support); no user-facing feature documentation, onboarding path, or documented limitations for this specific application. |
| 9 | Licensing, attribution, and responsible reuse | 4/10 | An MIT `LICENSE` file (St. Jude Children's Research Hospital BioHackathon, 2025) is present and clear, but there is no `CITATION.cff` and no attribution documented for third-party or generated media assets bundled in `public/` and `Image Projects/`. |
| 10 | Ethics, accessibility, and sustainability | 1/10 | Only one component (`src/views/Home.vue`) shows any `alt`/`aria-` usage; no accessibility statement, no ethics/privacy note despite health-themed comic content (e.g. `LordLeukemia`, `BMTTransplant` assets), and no maintenance/archival plan. |
| **Total** | | **24/100** | |

## Observations (evidence, separate from recommendations)

- The project is a Vue 3 + TypeScript + Vite + Vuetify single-page application
  ("typescript-bbq-boilerplate") that presents interactive comics/audio
  content, built during the St. Jude KIDS25 BioHackathon.
- `git log` (`8dafc28`): 47 commits, contributors `Jared Andrews`,
  `Michael Gattas`, `PepeRulo`, `ryanne-m`; no tags exist (`git tag` returns
  empty).
- `package.json`: scripts are `dev`, `build`, `preview`, `test`; dependencies
  include `vue`, `vuetify`, `pinia`, `vue-router`, `axios`, `webfontloader`;
  devDependencies include `vitest`, `@vue/test-utils`, `eslint`, `typescript`.
- No files found matching `*.spec.ts` / `*.test.ts` anywhere in the tree.
- No `.github/` directory exists at all (no workflows, issue templates, or
  PR templates).
- `LICENSE` is the MIT License, copyright St. Jude Children's Research
  Hospital BioHackathon (2025).
- `README.md` is limited to run instructions and unedited Vite/Vue
  scaffold documentation; it does not describe the project's purpose.

## Recommendations (cited to Turing Way guidance)

1. **Add tests that exercise the declared `vitest`/`@vue/test-utils`
   tooling.** The `test` script exists but nothing runs it against real
   code, so testing/validation is unverifiable.
   *Turing Way guidance:* [Testing Guidance](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/testing/testing-guidance.md)
2. **Add a CI workflow (e.g. GitHub Actions)** to run linting, type-checking
   (`vue-tsc`), and tests automatically on push/PR, since none currently
   exists.
   *Turing Way guidance:* [CI Practices](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/ci/ci-practices.md)
3. **Add `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and issue/PR templates.**
   With 4 active contributors and no documented review process, contribution
   norms are currently implicit only.
   *Turing Way guidance:* [Version Control](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/vcs.md)
4. **Rewrite `README.md`'s project section** to state the project's purpose,
   intended audience, and known limitations, rather than only run
   instructions and Vite template boilerplate.
   *Turing Way guidance:* [Guide for Project Design](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/project-design/project-design.md)
5. **Add a `CITATION.cff`** alongside the existing MIT `LICENSE`, and
   document provenance/attribution for bundled generated images and audio.
   *Turing Way guidance:* [Open Source](https://github.com/the-turing-way/the-turing-way/blob/bb3f7abb56a40cd92a654fb51e4ec91f429cca2a/book/website/reproducible-research/open/open-source.md)

## Limitations of this review

- This review is a static, point-in-time snapshot of the committed files and
  local `git log`; it does not reflect GitHub-hosted collaboration surfaces
  (open issues, discussions, branch protection rules, GitHub Actions run
  history) beyond what is committed to the repository.
- Scores reflect only directly observable repository evidence; no claims
  were taken on faith, and no criterion was skipped or merged with another.
- This snapshot must not be represented as an official Turing Way
  certification, endorsement, or institutional approval.

**Total score: 24 / 100**
