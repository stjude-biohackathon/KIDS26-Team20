---
name: turing-way-review
description: Review a research software repository against cited Turing Way practices and provide an evidence-based maturity rating with prioritized improvements
license: MIT
compatibility: opencode, claude-code, github-copilot
metadata:
  audience: research-teams-and-maintainers
  status: active
---

# Turing Way Review

## Use this skill when

A researcher, maintainer, or team asks to review a repository such as Pecan for
reproducible research, project design, version control, or research software
practices using The Turing Way.

## Do not use this skill when

The request requires a security audit, clinical validation, institutional-policy
approval, legal advice, access to a private repository without authorization,
or modification of the reviewed repository without a separate implementation
request.

## Required tools

- `learning-assistant_list_resources`
- `learning-assistant_get_resource`
- `learning-assistant_get_turing_way_evidence_packets`
- `learning-assistant_get_turing_way_review_evidence`
- `learning-assistant_render_validated_turing_way_review`

## Review workflow

1. Confirm the repository's local path or public GitHub URL, its purpose, and
   whether the requester wants a broad baseline review or a specific focus.
   Do not request, open, or report PHI, credentials, private URLs, or ignored
   local configuration.
2. Inspect the repository's tracked documentation, version-control metadata,
   automation, dependency manifests, tests, and contributor guidance. Do not
   execute untrusted repository scripts merely to perform the review.
3. Call `learning-assistant_get_turing_way_review_evidence` before reading or
   scoring the repository. This required tool runs focused MyGPT RAG queries
   for project design, reproducibility, and version-control collaboration
   against the `turing-way` dataset. Use only its returned context and source
   records as evidence for best-practice claims.
4. Call `learning-assistant_list_resources`, then
   `learning-assistant_get_resource` for the relevant Turing Way resources
   before assigning any ratings. Use the returned pinned GitHub URLs as
   citations for the RAG-grounded findings. Retain the `relevance_score`
   returned for the relevant review area.
5. Draft evidence-backed score rows for each review area. Each row must contain
   exactly one directly observed claim or clearly labeled reviewer inference
   and its exact repository evidence URL. If an area rationale needs multiple
   facts, use separate rows; do not hide unsupported claims in a summary.
   Withhold all area scores and the total if any rationale lacks its required
   repository evidence.

   | Area | 0 - absent | 1 - developing | 2 - established |
   | --- | --- | --- | --- |
   | Project design | Purpose and scope are unclear | Purpose or contribution path is documented | Purpose, scope, contributors, and decision process are clear |
   | Reproducibility | No repeatable setup or validation path | Partial setup, environment, or test instructions | Repeatable setup, pinned dependencies, and documented validation |
   | Version control and collaboration | No visible contribution or history guidance | Basic Git or contribution guidance | Clear contribution workflow, review expectations, and change traceability |

6. Only after every score rationale has its direct evidence, assign its area
   score. Do not calculate a total or rating label, and do not render a score
   table yourself. The canonical renderer calculates and renders those values.
7. Draft no more than five single-focus recommendations, then call
   `learning-assistant_get_turing_way_evidence_packets` once with one request
   per recommendation. Each request must contain the recommendation claim,
   the exact `resource_id` for its supporting Turing Way chapter, and its
   directly observed repository fact plus the exact, direct public GitHub URL
   that proves that fact. Pass exactly one `repository_fact` in each request.
   Each recommendation and fact entry must describe one fact only. For a
   multi-part finding, provide separate fact entries and a separate proving URL
   for every part; a related or nearby file is not evidence for an unshown
   fact. A positive file URL proves only the content it displays and must not
   be used to prove the absence of unrelated files. Each separately asserted
   absence requires its own repository-fact entry and exact tree or API-listing
   URL, unless one exact GitHub recursive-tree or API listing demonstrably
   covers every claimed path at the checked commit. Use the exact commit SHA,
   never a mutable branch or tag. Before relying on a recursive API listing,
   confirm that its response has `"truncated": false`; a truncated listing does
   not establish absence. A GitHub `/tree/COMMIT` page is not recursive-tree
   API evidence and must not be used for an absence claim. A single commit page proves only that commit's
   content; use a commit-pinned history page
   (`https://github.com/OWNER/REPOSITORY/commits/COMMIT`) for a claim about
   the history reachable from that commit. Do not infer the absence of
   branches or tags from either URL. Use only the returned packet's
   citation and matching relevance score;
   the three area-level queries cannot substitute for this step.
   An absence in an existing file's content (for example, a README omitting a
   dataset URL) is not a tree absence: cite that file's commit-pinned
   `/blob/COMMIT/PATH` URL instead.
8. Do not invent expected benefits or explanatory prose for recommendations.
   The claim, observed repository fact, resolved Turing Way citation, and
   MyGPT relevance score are the complete recommendation evidence.
   Do not estimate, normalize, omit, or invent a relevance score.
9. Call `learning-assistant_render_validated_turing_way_review` with exactly
   three score rows and the complete packets returned by
   `learning-assistant_get_turing_way_evidence_packets`. This tool subsumes
   `learning-assistant_validate_turing_way_review`: it validates the inputs,
   calculates the total and label, and renders the canonical report. The final
   response must contain exactly its returned `report` field, verbatim. Do not
   render `score_section` or `recommendation_evidence_block` separately. Do
   not add an agent-written introduction, repository narrative, RAG table,
   summary, conclusion, notice, or trailing text. Never manually calculate,
   rewrite, or reformat a score, rationale, repository fact, citation,
   relevance score, or recommendation. A rendered rating is a transparent
   snapshot, not a certification.
10. Recommend no more than five improvements. Do not combine unrelated changes
   (for example, a contribution guide and `.gitignore`) in one recommendation.
   Prioritize low-risk, high-impact
   improvements that a research team can verify, such as a reproducible setup
   command, dependency pinning, test instructions, a contribution guide, or
   a documented project scope.

## Final response

The renderer's `report` is the complete and only final response. It
intentionally covers only the validated score and recommendation-evidence
sections; do not add repository narrative or any other report section.

## Failure behavior

If the repository path or public URL is unavailable, state that review access is required.
If the required MyGPT RAG evidence or a Turing Way resource lookup fails, explain that no
evidence-based rating can be given and do not substitute invented standards or
citations. If the repository contains restricted content, exclude it from the
review and say that the review is limited to accessible, non-sensitive files.
If a relevance score cannot be associated with every cited recommendation, do
not assign a rating or call the result a Turing Way-grounded review.

## Evaluation cases

- Positive: "Review the checked-out Pecan repository against Turing Way best
  practices and give it a rating with the most important improvements."
- Positive: "Assess this analysis repository's reproducibility documentation
  and cite the relevant Turing Way guidance."
- Negative: "Penetration-test this repository and rate its security."
- Negative: "Approve this project as compliant with St. Jude policy."
