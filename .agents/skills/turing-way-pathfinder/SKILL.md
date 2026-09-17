---
name: turing-way-pathfinder
description: Select a Turing Way role pathway and a short, cited checklist for a scientist's current research goal
license: MIT
compatibility: opencode, claude-code, github-copilot
metadata:
  audience: scientists-and-research-teams
  status: active
---

# Turing Way Pathfinder

## Use this skill when

A scientist, researcher, data steward, project lead, or research software
engineer asks where to begin with The Turing Way, wants a learning path, or
needs a short checklist for their current research goal.

## Do not use this skill when

The requester asks for an institutional-policy decision, clinical or legal
advice, a security audit, or asks the assistant to collect personal or
sensitive information.

## Required tools

- `learning-assistant_list_resources`
- `learning-assistant_get_resource`
- `learning-assistant_get_turing_way_evidence_packets`

## Intake and pathway selection

1. Extract the role and immediate goal when the requester already gave them.
   Ask the missing question or questions only when that information is absent.
   Then ask for the current project stage if it was not provided. This required
   follow-up makes the selected checklist actionable. Do not ask about the
   requester's private life, identity, employer, patients, or research data:
   - **Which role best matches your current work?** Early-career researcher,
     project leader, research software engineer, data steward,
     community/collaboration maintainer, or unsure.
   - **What do you need to do now?** Start/design a project, make work
     reproducible, organize/share data, improve research code, prepare a
     paper or software release, collaborate, or review a repository.
   - **Where are you in this project?** Starting, analysis underway, or
     preparing to share/publish.
2. If the requester is unsure, select the pathway from their immediate goal,
   state that assumption, and let them correct it. Do not block on a perfect
   label.
3. Select one primary pathway:

   | Role or goal | Turing Way pathway | First focus |
   | --- | --- | --- |
   | New researcher or broad foundations | Early Career Researchers | Project checklist, Git/GitHub, methods, data management, ethics |
   | Planning, allocating resources, or coordinating a team | Project Leaders | Scope, project repository, versioning, reproducibility |
   | Maintaining research code or pipelines | Research Software Engineers | Testing, environments, CI, review, licensing |
   | Managing, documenting, or sharing research data | Data Stewards | FAIR data, metadata, storage, sharing, data security |
   | Preparing a release, software paper, or citation record | Software Citation | Citation, licensing, release and archival metadata |
   | Growing a contributor community | Community Management | Governance, contributor process, accessible collaboration |
   | Cross-institution or cross-discipline collaboration | Data Science Without Borders | Inclusive collaboration and communication |

4. Call `learning-assistant_list_resources`, then
   `learning-assistant_get_resource` for the selected pathway's exact resource
   ID before drafting actions:

   | Turing Way pathway | Required resource ID |
   | --- | --- |
   | Early Career Researchers | `turing-way:book/website/pathways/pathways-early-career-researchers` |
   | Project Leaders | `turing-way:book/website/pathways/pathways-project-leaders` |
   | Research Software Engineers | `turing-way:book/website/pathways/pathways-research-software-engineers` |
   | Data Stewards | `turing-way:book/website/pathways/pathways-data-stewards` |
   | Software Citation | `turing-way:book/website/pathways/pathways-software-citation` |
   | Community Management | `turing-way:book/website/pathways/pathways-community-management-concepts` |
   | Data Science Without Borders | `turing-way:book/website/pathways/pathways-data-science-without-borders` |

   Then retrieve the exact supporting chapters needed for the immediate goal.
   Cite only their returned pinned URLs.
5. Use the project stage to sequence the checklist: foundations and setup for
   **starting**; environment capture, workflow automation, and validation for
   **analysis underway**; documentation, sharing, citation, and archival work
   for **preparing to share/publish**.
6. Draft three to five practical checklist actions. Call
   `learning-assistant_get_turing_way_evidence_packets` with one focused
   claim and one exact supporting `resource_id` per action before giving the
   checklist. Use only each returned packet's citation and relevance score.

## Required response format

Return:

1. **Your Turing Way path:** selected pathway and the role, goal, and project
   stage inputs used.
2. **Why this path:** a two-sentence explanation, including any assumption.
3. **Start here:** three to five ordered actions sized for the requester's
   current goal. Every action must include a pinned Turing Way citation and
   its exact `MyGPT RAG relevance: N%` value returned for that action.
4. **Next checkpoint:** one observable outcome that lets the requester know
   they completed the first step.

The returned relevance value indicates the match between the MyGPT retrieval
query and Turing Way evidence; it is not a measure of the person's skill,
project quality, or compliance.

Every pathway label, chapter title, URL, and quoted statement must match the
resource returned by `learning-assistant_get_resource`. Do not use a resource
from a different Turing Way section, reuse one URL for unrelated chapters, or
invent a chapter title from a MyGPT source-record label.

## Failure behavior

If Turing Way resource retrieval or targeted MyGPT claim evidence fails, say
that a cited pathway cannot be produced and do not invent citations, scores,
or a checklist presented as Turing Way guidance. Provide no more than one
general next step: restore the local RAG service and run `get_rag_status`.

## Evaluation cases

- Positive: "I am a new PhD student and need to make my analysis reproducible.
  Where should I start?"
- Positive: "I am a new PhD student, my analysis is underway, and I need to
  make it reproducible."
- Positive: "I maintain our genomics pipeline and need a practical Turing Way
  checklist for its next release."
- Positive: "I am unsure of my role, but need to share a dataset responsibly."
- Negative: "Decide whether my patient dataset complies with institutional
  policy."
- Negative: "Tell me what career I should pursue."
