---
name: mygpt-library
description: Find a scientist's approved MyGPT datasets and document titles through the configured MyGPT API
license: MIT
compatibility: opencode, claude-code, github-copilot
metadata:
  audience: scientists-and-trainees
  status: active
---

# MyGPT Library

## Use this skill when

A scientist asks to list their MyGPT libraries, document titles, or retrieve
evidence from an approved MyGPT dataset.

## Do not use this skill when

The request needs a generated scientific answer, uploads or changes to a
library, clinical interpretation, or access to someone else's data.

## Required tools

- `learning-assistant_list_mygpt_datasets`
- `learning-assistant_list_mygpt_documents`
- `learning-assistant_query_mygpt_context`

## Workflow

1. Confirm the user's email address only when the client cannot supply it from
   an approved authenticated identity.
2. Call `learning-assistant_list_mygpt_datasets` with that email address.
3. Ask the user to select a dataset when more than one is relevant.
4. Call `learning-assistant_list_mygpt_documents` with the same email address
   and selected dataset.
5. For a question about a selected dataset, call
   `learning-assistant_query_mygpt_context` and return its context and source
   records as MyGPT evidence. Do not treat the evidence as institutional policy.

## Failure behavior

If MyGPT is not configured or does not respond, explain that an approved
`MYGPT_BASE_URL` is required. Explain that question retrieval also requires
`MYGPT_MODEL_ID` and a MyGPT dataset containing the requested material. Do not
retry against an unapproved endpoint or invent library contents, sources, or
citations.

## Evaluation cases

- Positive: a researcher asks which MyGPT datasets are available to them.
- Positive: a researcher selects a dataset and asks for its document titles.
- Positive: a researcher asks a question answered by a Turing Way dataset in MyGPT.
- Negative: a researcher asks to upload a paper or change a MyGPT dataset.
- Negative: a researcher asks for another person's private library.
