---
name: turing-way-certified
description: Explain Turing Way certification claims and produce a cited 100-point readiness review with Markdown and PDF reports without misrepresenting guidance as official certification
license: MIT
compatibility: opencode, claude-code, github-copilot
metadata:
  audience: research-teams-and-maintainers
  status: active
---

# Turing Way Certified

## Use this skill when

A researcher, maintainer, or team asks whether a project is “Turing Way
certified,” wants to claim compliance with The Turing Way, or requests a
Turing Way-aligned certification or readiness assessment.

## Do not use this skill when

The request is for a security audit, clinical or patient-data assessment,
institutional-policy approval, legal certification, or a general learning path
that does not involve a certification claim.

## Required tools

- `learning-assistant_list_resources`
- `learning-assistant_get_resource`
- `learning-assistant_get_turing_way_review_evidence`
- `learning-assistant_get_turing_way_evidence_packets`
- Local file search, reading, and non-destructive command tools
- A PDF-capable local renderer such as Pandoc, LibreOffice, or a Python PDF
  library
  
## Ten-criterion rubric

Score every criterion from 0 to 10 using observable evidence. The total is out
of 100. Do not award points for claims that cannot be verified in the reviewed
repository. A score of 0 means no reliable evidence was found, 5 means the
practice is partially or inconsistently documented, and 10 means the practice
is clear, repeatable, and maintained. Use intermediate scores only when the
evidence supports them, and explain the reason.

1. **Project purpose and scope:** clear research question or project purpose,
   scope, intended users, and known limitations.
2. **Version control and provenance:** meaningful Git history, traceable
   changes, tagged or pinned releases where appropriate, and preserved
   provenance.
3. **Open collaboration:** contribution guidance, issue or discussion paths,
   review expectations, code of conduct, and maintainership information.
4. **Reproducible environments:** setup instructions, declared and
   appropriately pinned dependencies, supported versions, and environment
   capture.
5. **Data and workflow provenance:** documented inputs and outputs, data
   sources, schemas or metadata, workflow steps, and handling of generated
   artifacts.
6. **Testing and validation:** automated or documented tests, validation
   criteria, representative fixtures, and clear instructions for reproducing
   checks.
7. **Automation and continuous integration:** useful CI or equivalent
   automation for tests, quality checks, packaging, or reproducibility, with
   failures visible to contributors.
8. **Documentation and usability:** accurate README and user/developer
   documentation, examples, onboarding path, and documentation of limitations.
9. **Licensing, attribution, and responsible reuse:** an identifiable license,
   third-party attribution, citation guidance, and appropriate reuse terms.
10. **Ethics, accessibility, and sustainability:** relevant ethical or privacy
    considerations, accessible project practices, resource or sustainability
    considerations, and a plan for maintenance or archival.

Use the Turing Way evidence tools before assigning scores. Treat the Turing Way
as public best-practice guidance, not as a certification authority or
institutional policy. Keep repository observations separate from
recommendations.

## Workflow

1. State clearly that a Turing Way-aligned review is not an official
   certification unless the requester provides an authorized certification
   program and its criteria.
2. Inspect only the accessible, non-sensitive repository documentation,
   environment, tests, version-control guidance, and automation relevant to
   the requested scope.
3. Call `learning-assistant_get_turing_way_review_evidence`, then use
   `learning-assistant_list_resources` and `learning-assistant_get_resource` to
   retrieve the relevant pinned Turing Way guidance.
   For listing, start with `limit: 200, offset: 0`; advance `offset` by the
   returned entry count until the needed resources are found or a page has
   fewer than 200 entries. Do not infer that a resource is absent from the
   first page.
4. For each proposed readiness recommendation, call
   `learning-assistant_get_turing_way_evidence_packets` with one focused claim,
   one exact `resource_id`, and one directly observed repository fact with its
   exact public GitHub URL.
5. Score every criterion in the ten-criterion rubric above. Use every
   criterion once so the result is always an integer score out of 100; do not
   substitute the three-area, six-point `turing-way-review` renderer.
6. Write `TURING_WAY_CERTIFICATION.md` at the reviewed repository root when it
   is writable. Include the review date, scope, confidence, all ten criterion
   scores, evidence, checks, recommendations, pinned citations, limitations,
   and the exact total in the form `X / 100`.
7. Render that Markdown report to
   `TURING_WAY_CERTIFICATION.pdf` using an available PDF-capable local tool.
   Preserve every Markdown table in the PDF as a readable PDF table with its
   header row, columns, and cell contents; never skip or flatten tables while
   converting. Verify that the file exists, is non-empty, and contains the report's score table
   before reporting both artifact paths and the total score. If the repository is read-only, write both artifacts to the session
   artifact directory instead. If no PDF renderer can preserve tables, state
   the failure explicitly and do not claim that a valid PDF was generated.
8. Describe the result as a transparent readiness snapshot, never as
   certification. A score is not an official Turing Way certification.

## Failure behavior

If repository access, required evidence, or a pinned source is unavailable,
say so plainly and do not assign a certification status or invent criteria.
Exclude credentials, PHI, private URLs, and restricted files. Never invent
citations, repository facts, relevance scores, category weights, or a PDF
artifact. If a required ten-criterion score, score table, or table-preserving PDF cannot
be produced, return the blocking reason instead of a partial or
success-shaped report.

## Evaluation cases

- Positive: “Can you tell me whether this research repository is Turing Way
  certified and what it still needs?”
- Positive: “Give our team a Turing Way-aligned readiness assessment with
  citations, a score out of 100, and Markdown/PDF reports including the score
  table in the PDF.”
- Positive: “Save the certification-readiness report as a PDF and show me the
  artifact path and total score.”
- Negative: “Penetration-test this repository and certify its security.”
- Negative: “Choose a beginner Turing Way pathway for my analysis.”
