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
5. Score each review area from 0 to 2 using observed repository evidence:

   | Area | 0 - absent | 1 - developing | 2 - established |
   | --- | --- | --- | --- |
   | Project design | Purpose and scope are unclear | Purpose or contribution path is documented | Purpose, scope, contributors, and decision process are clear |
   | Reproducibility | No repeatable setup or validation path | Partial setup, environment, or test instructions | Repeatable setup, pinned dependencies, and documented validation |
   | Version control and collaboration | No visible contribution or history guidance | Basic Git or contribution guidance | Clear contribution workflow, review expectations, and change traceability |

6. Add the three area scores for a rating out of 6. Label 0-1 as
   **Starting**, 2-3 as **Developing**, 4-5 as **Established**, and 6 as
   **Strong foundation**. This is a transparent snapshot, not a certification.
7. Draft no more than five recommendations, then call
   `learning-assistant_get_turing_way_evidence_packets` once with one request
   per recommendation. Each request must contain the recommendation claim,
   the exact `resource_id` for its supporting Turing Way chapter, and its
   directly observed repository fact plus the exact, direct public GitHub URL
   that proves that fact. Each fact entry must describe one fact only. For a
   multi-part finding, provide separate fact entries and a separate proving URL
   for every part; a related or nearby file is not evidence for an unshown
   fact. A positive file URL proves only the content it displays and must not
   be used to prove the absence of unrelated files. Each separately asserted
   absence requires its own repository-fact entry and exact tree or API-listing
   URL, unless one exact GitHub recursive-tree or API listing demonstrably
   covers every claimed path at the checked commit. Use the exact commit SHA,
   never a mutable branch or tag. Before relying on a recursive API listing,
   confirm that its response has `"truncated": false`; a truncated listing does
   not establish absence. Use only the returned packet's
   citation and matching relevance score;
   the three area-level queries cannot substitute for this step.
8. Return a concise report containing the rating, evidence observed, gaps,
   prioritized improvements, expected benefit, and a Turing Way citation for
   each recommendation. Every recommendation must display the corresponding
   MyGPT result as `MyGPT RAG relevance: N%` beside its citation, where `N`
   is the returned `relevance_score` formatted as a percentage. Do not
   estimate, normalize, omit, or invent a relevance score. If MyGPT returns
   no relevance score, write `MyGPT RAG relevance: not provided` rather than
   presenting a percentage. Separate confirmed facts from assumptions.
9. Recommend no more than five improvements. Prioritize low-risk, high-impact
   improvements that a research team can verify, such as a reproducible setup
   command, dependency pinning, test instructions, a contribution guide, or
   a documented project scope.

## Required report format

Use this format for every completed review:

```markdown
### Repository evidence

_Sourced only from direct, commit-pinned repository inspection (GitHub
file/tree/API URLs), never from MyGPT retrieval._

- **Fact:** Tests are documented in the contributor guide.
  **Evidence:** [Exact file proving the content claim](https://github.com/OWNER/REPOSITORY/blob/COMMIT/CONTRIBUTING.md)
- **Gap:** No issue template is present.
  **Evidence:** [Exact repository tree or complete, non-truncated API listing covering the checked commit](https://github.com/OWNER/REPOSITORY/tree/COMMIT/.github)

### RAG evidence

_MyGPT relevance scores support the Turing Way citation choice only; they are
not evidence about the reviewed repository. The MCP resource tool resolves the
pinned Turing Way URL._

| Review area | MyGPT RAG relevance | Turing Way source |
| --- | --- | --- |
| Reproducibility | 94% | [Pinned chapter title](https://github.com/...) |

### Prioritized improvements

1. **Improvement title** — observed repository gap and expected benefit.
   Citation: [Pinned Turing Way chapter](https://github.com/...) —
   `MyGPT RAG relevance: 94%`
```

The relevance value for every evidence row and recommendation must be copied
from its matching evidence packet. A
standalone bibliography, an uncited improvement, or a citation without its
relevance label is incomplete and must not be presented as a Turing
Way-grounded review.

Render the returned packet's `repository_fact` separately from its Turing Way
citation. State that every content claim uses the exact public GitHub file or
commit URL that shows its content, and every absence claim uses the exact
public GitHub repository tree or API listing URL that covers the searched
scope and ref. A positive file URL must not be used as absence evidence for an
unrelated path. Use distinct repository-fact entries and URLs for separately
asserted absences, unless one exact GitHub recursive-tree or API listing
demonstrably covers all claimed paths at the checked commit. Never cite a
mutable branch or tag: use the exact commit SHA. A recursive API listing is
adequate only when its response confirms `"truncated": false`. Label deductions
as reviewer inferences rather than source facts. MyGPT provides retrieval
evidence and relevance; the MCP resource tool resolves the pinned Turing Way
URL. A Turing Way citation supports the recommendation; it does not prove a
claim about the reviewed repository.

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
