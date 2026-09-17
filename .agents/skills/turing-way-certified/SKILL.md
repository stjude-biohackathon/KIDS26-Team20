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
4. For each proposed readiness recommendation, call
   `learning-assistant_get_turing_way_evidence_packets` with one focused claim,
   one exact `resource_id`, and one directly observed repository fact with its
   exact public GitHub URL.
5. Score the complete eight-category rubric in
   `.agents/skills/turing-healthcheck-prototype/references/rubric.md`. Use
   every category and its prescribed weight so the result is always an
   integer score out of 100; do not substitute the three-area, six-point
   `turing-way-review` renderer.
6. Write `TURING_WAY_CERTIFICATION.md` at the reviewed repository root when it
   is writable. Include the review date, scope, confidence, all eight category
   scores and weights, evidence, checks, recommendations, pinned citations,
   limitations, and the exact total in the form `X / 100`.
7. Render that Markdown report to
   `TURING_WAY_CERTIFICATION.pdf` using an available PDF-capable local tool.
   Verify that the file exists and is non-empty, and report both artifact paths
   and the total score. If the repository is read-only, write both artifacts
   to the session artifact directory instead. If no PDF renderer is available,
   state the failure explicitly and do not claim that a PDF was generated.
8. Describe the result as a transparent readiness snapshot, never as
   certification. A score is not an official Turing Way certification.

## Failure behavior

If repository access, required evidence, or a pinned source is unavailable,
say so plainly and do not assign a certification status or invent criteria.
Exclude credentials, PHI, private URLs, and restricted files. Never invent
citations, repository facts, relevance scores, category weights, or a PDF
artifact. If a required eight-category score or PDF cannot be produced, return
the blocking reason instead of a partial or success-shaped report.

## Evaluation cases

- Positive: “Can you tell me whether this research repository is Turing Way
  certified and what it still needs?”
- Positive: “Give our team a Turing Way-aligned readiness assessment with
  citations, a score out of 100, and Markdown/PDF reports.”
- Positive: “Save the certification-readiness report as a PDF and show me the
  artifact path and total score.”
- Negative: “Penetration-test this repository and certify its security.”
- Negative: “Choose a beginner Turing Way pathway for my analysis.”
