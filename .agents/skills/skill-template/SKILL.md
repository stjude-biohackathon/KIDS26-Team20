---
name: skill-template
description: Template for creating a tested learning-assistant skill with clear triggers and MCP dependencies
license: MIT
compatibility: opencode, claude-code, github-copilot
metadata:
  audience: contributors
  status: template
---

# Skill Template

## Use this skill when

Describe the user request that should trigger this skill.

## Do not use this skill when

Describe adjacent requests that belong to another workflow.

## Required tools

List the MCP tools this skill depends on. The server currently provides two:

- `learning-assistant_list_resources`
- `learning-assistant_get_resource`

## Workflow

1. Ask only for information required to understand the learner's goal.
2. Call the required MCP tools rather than inventing sources.
3. Present recommendations in accessible language with source links.
4. State uncertainty and distinguish general guidance from institutional policy.

## Failure behavior

If a lookup fails, explain the failure and suggest a retry. Do not fabricate
resources, citations, or policy.

## Evaluation cases

- Positive: a learner asks for guidance matching the trigger above.
- Negative: a request falls under the non-goals above.
