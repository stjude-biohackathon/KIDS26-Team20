---
name: turing-way-guidance
description: Give a scientist an accessible, citation-backed learning path for reproducible research, data science, or AI practices using The Turing Way
license: MIT
compatibility: opencode, claude-code, github-copilot
metadata:
  audience: scientists-and-trainees
  status: active
---

# Turing Way Guidance

## Use this skill when

A scientist, trainee, or research team asks where to begin with reproducible
research, data science, research software, AI practice, or collaboration.

## Do not use this skill when

The request needs institutional policy, patient data, a clinical decision, or
content not supported by the approved learning-resource corpus.

## Required tools

- `learning-assistant_list_resources`
- `learning-assistant_get_resource`
- `learning-assistant_get_turing_way_evidence_packets`

## Workflow

1. Identify the learner's goal and experience level from their request. Ask for
   only the missing detail needed to make a recommendation.
2. Call `learning-assistant_list_resources` and select relevant resources.
3. Call `learning-assistant_get_resource` for the selected resources before
   making claims about their content.
4. Draft one to five practical next steps, then call
   `learning-assistant_get_turing_way_evidence_packets` with one focused claim
   and one exact supporting `resource_id` per step.
5. Give ordered, practical next steps using only the citation and relevance
   score from each returned evidence packet. Display
   `MyGPT RAG relevance: N%` for every recommendation. Distinguish public
   Turing Way guidance from St. Jude policy.

## Failure behavior

If an MCP lookup fails or has no relevant resource, say so plainly and offer a
retry or a narrower search. Do not invent sources, citations, relevance scores,
institutional policy, or model output.

## Evaluation cases

- Positive: a wet-lab scientist asks for a beginner-friendly path to make an
  analysis reproducible.
- Positive: a new research software engineer asks for guidance on collaborative
  coding practices.
- Negative: a user asks whether an institutional data policy permits a
  particular dataset.
- Negative: a user provides clinical or patient information for interpretation.
