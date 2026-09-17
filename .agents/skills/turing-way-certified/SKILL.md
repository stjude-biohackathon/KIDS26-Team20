---
name: turing-way-certified
description: Rate a public GitHub repository against ten evidence-based Turing Way alignment criteria and generate a citation-backed PDF report with scores, findings, limitations, and prioritized improvements. Use when a user asks for a Turing Way score, certification-style assessment, reproducibility rating, or PDF review of a public GitHub project.
license: MIT
compatibility: Requires a public GitHub repository, Git, file inspection, public commit-pinned GitHub evidence URLs, and a PDF-capable local reporting path.
metadata:
  audience: research-software-teams-and-maintainers
  status: draft
---

# Turing Way Certified

## Use this skill when

Use this skill when a user asks to assess, rate, score, or produce a PDF report
about how closely a public GitHub repository follows
reproducible, open, ethical, and collaborative research-software practices
described by The Turing Way. This skill produces an alignment assessment, not
an official certification, accreditation, compliance determination, or
institutional approval.

## Do not use this skill when

Do not use this skill for penetration testing, a security audit, clinical or
HIPAA validation, legal or licensing advice, institutional-policy approval,
reviewing a private or local-only repository, or changing the reviewed
repository. The evidence-packet tools require public, commit-pinned GitHub
URLs, so private and local-only evidence cannot support this assessment. Do not
expose credentials, private URLs, PHI, patient identifiers, or other restricted
content in the report. Use a normal implementation workflow when the user wants
code changes rather than an assessment.

## Required tools

- `learning-assistant_get_turing_way_review_evidence`
- `learning-assistant_list_resources`
- `learning-assistant_get_resource`
- `learning-assistant_get_turing_way_evidence_packets`
- `learning-assistant_render_validated_turing_way_review`
- Repository file inspection and non-destructive Git commands
- A local PDF-capable reporting path. Prefer an existing repository-supported
  PDF tool; otherwise create a self-contained HTML or Markdown source and use
  an installed PDF converter. Never download dependencies or send repository
  contents to an unapproved external service.

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

1. Confirm the exact public GitHub URL (`OWNER/REPOSITORY`), the commit or ref
   to assess, and whether the user wants the default whole-repository review.
   If the ref is not specified, use the repository's default branch and record
   the resolved commit SHA. A local checkout may be used for inspection only
   when it corresponds to that public repository and every cited fact can be
   proven with a public, commit-pinned GitHub evidence URL. Do not review a
   private or local-only repository.
2. Explain that the result is a 100-point Turing Way alignment assessment, not
   official certification. State the review date, repository/ref/commit, and
   accessible scope before collecting evidence.
3. Call `learning-assistant_get_turing_way_review_evidence`, then call
   `learning-assistant_list_resources` and
   `learning-assistant_get_resource` for the relevant returned resources.
   Use only returned context and pinned source records for Turing Way claims.
4. Inspect the public repository, or a matching local checkout of the same
   public commit, including repository instructions, README and documentation, Git history,
   manifests and lockfiles, source and workflow configuration, tests, issue and
   contribution guidance, license and citation files, data/workflow metadata,
   and accessibility or ethics documentation. Exclude caches, vendored code,
   build output, binaries, secrets, and restricted content.
5. Run only documented, local, non-destructive checks that are relevant and
   safe. Do not install dependencies, deploy code, mutate data, use
   credentials, or enable optional network tests. Record every check, exit
   status, and meaningful output; a failed check is evidence and does not stop
   independent inspection.
6. For each of the ten criteria, record: score from 0-10, observed evidence
   with exact file/line or commit-pinned GitHub URL, rationale, confidence,
   and one concrete improvement when the score is below 10. Use conservative
   scores when evidence is unavailable. Do not infer that a file or practice
   is absent from a single positive file URL; use a commit-pinned tree or API
   listing for absence claims and confirm recursive API listings are not
   truncated.
7. Draft no more than five highest-impact improvements. For each improvement,
   call `learning-assistant_get_turing_way_evidence_packets` with its exact
   recommendation, one directly observed repository fact, its exact
   commit-pinned public GitHub evidence URL, and the matching `resource_id`.
   Do not invent relevance scores, citations, or expected benefits.
8. Call `learning-assistant_render_validated_turing_way_review` with the
   required evidence packets and score rows when its contract applies. Do not
   manually present a competing Turing Way rating or alter returned citations.
   If that renderer cannot represent all ten criteria, preserve its validated
   evidence and use the same source records in the expanded PDF table without
   fabricating a canonical rating.
9. Build a PDF containing, in this order: title and review date; repository,
   ref, commit, and scope; a 100-point score and confidence; a ten-row score
   table; detailed evidence and exact citations; checks run; prioritized
   improvements; Turing Way sources; and limitations. Include the scoring rule
   and a prominent statement that this is not official certification.
10. Save the PDF as `TURING_WAY_CERTIFIED_REPORT.pdf` in the reviewed
    repository root when writable. Also save the report source as
    `TURING_WAY_CERTIFIED_REPORT.md` or `.html` so the PDF is auditable. If the
    workspace is read-only, return the generated artifact through the
    supported attachment/output mechanism and state that the repository files
    could not be written.
11. Verify that the PDF exists, is non-empty, opens or passes the available
    PDF validation check, contains all ten criteria and the total score, and
    preserves source repository, path, ref, and URL for every citation.

## Scoring and reporting rules

- Calculate `total = sum(score_1 ... score_10)` and report it as `N/100` and
  `N%`; do not call it a certification level.
- Report an overall confidence of high, medium, or low with a reason based on
  public evidence coverage and checks that actually ran.
- Distinguish observed facts, reviewer inferences, recommendations, and
  Turing Way guidance.
- Cite the exact repository commit, path, ref, and URL. Prefer line-specific
  blob URLs for file evidence and commit-pinned API/tree URLs for absence.
- Never inspect or include private repository content, secrets, tokens, private
  URLs, PHI, or patient identifiers.
- If a criterion is not applicable, score it 0 only if the lack of
  applicability is itself justified; otherwise mark it "insufficient evidence"
  and lower confidence rather than silently excluding it.
- Do not claim that a score means scientific validity, security, legal
  compliance, or institutional endorsement.

## Failure behavior

If the repository is private or local-only, explain that the evidence-packet
contract requires public, commit-pinned GitHub URLs and do not score it. If the
public repository cannot be accessed or the ref cannot be resolved, do not
score it. If Turing Way retrieval or resource resolution fails, do not invent
citations or present the result as evidence-backed; report the failure and stop
before assigning a rating. If a check, PDF converter, or output write fails,
record the exact failure, preserve the source report when possible, and do not
claim that a PDF was generated. If public evidence is incomplete, continue
independent inspection, lower confidence, and label the affected criteria
provisional. Never silently replace a missing source with a remembered URL or
an unverified standard.

## Evaluation cases

- Positive: "Rate this public GitHub repository against ten Turing Way
  criteria and generate a PDF report with citations."
- Positive: "Assess our research software project's reproducibility and
  collaboration practices out of 100 at this commit, then export the report
  as a PDF."
- Positive: "Give me a certification-style Turing Way readiness report, but
  clearly distinguish it from official certification."
- Negative: "Penetration-test this repository and certify it as secure."
- Negative: "Approve this repository for HIPAA or institutional compliance."
- Negative: "Rate this private or local-only repository without publishing its
  evidence."
- Negative: "Fix the repository's failing tests and update its workflows."
