---
name: profile-creator
description: Interviews a learner to build a local user profile (role, goals, focus areas, depth preference) that other skills can read to tailor guidance. Use when a user asks to set up, create, or update their learning profile or preferences.
license: MIT
compatibility: opencode, claude-code, github-copilot
metadata:
  audience: contributors
  status: draft
---

# Profile Creator

## Use this skill when

- A user asks to create, set up, edit, or update a personal learning profile
  or preferences for this assistant.

## Do not use this skill when

- A profile already exists and the user is just asking a normal question. Use
  the `profile-loader` skill (or read the existing profile file directly) instead of re-running the interview.
- The request is about Turing Way content or citations. Use
  `turing-way-resource-finder` or the MCP tools for that.
- The user asks to delete or reset their profile only. Handle that as a
  short, separate action (see Deleting a profile below), not a full
  interview.

## Where the profile lives

Write the profile to `config/profile.local.yaml` at the repository root.

- This path is gitignored; never commit it, print its full contents into a
  chat log meant for sharing, or copy it into any tracked file.
- If the file does not exist, create it. If it exists, show the user the
  current values before changing them, and update only the fields they want
  changed.
- Treat the contents as personal information about the user, not project
  data. Never reference another person's profile file. Never include patient
  data, PHI, or institutional-confidential content, consistent with the
  project's data rules.

## Profile schema

Collect only these fields. Leave a field unset (omit the key) rather than
guessing when the user has not answered it.

```yaml
# config/profile.local.yaml
role: ""              # e.g. "wet-lab biologist", "grad student", "RSE"
field: ""              # e.g. "genomics", "clinical research", "software"
work_type: ""          # one of: research, software, teaching, student, other
current_project: ""    # one short sentence, optional
goals: []              # short list, e.g. ["learn reproducible pipelines"]
recurring_tasks: []    # short list of tasks the user wants recurring help with
topics_of_interest: [] # short list
topics_to_deemphasize: [] # short list; do not raise these unprompted
depth: ""              # one of: brief, standard, in-depth
weaknesses_to_address: [] # short list, only if the user volunteers this
privacy_opt_out: false # true means: skip the in-depth/detailed interview below
```

## Workflow

1. Ask whether the user wants the full interview or a quick, minimal setup.
   If they choose minimal, or set `privacy_opt_out: true`, collect only
   `role`, `work_type`, and `depth`, and skip the rest.
2. Ask one question at a time, in plain language, in this order:
   role/profession/field, type of work, current project or goal, recurring
   tasks they want help with, topics they care about, topics to
   de-emphasize, any weaknesses or gaps they want addressed, and how much
   depth they want in answers (brief, standard, or in-depth).
3. At any point, if the user declines a question or asks to stop, record
   what has been answered so far, leave the rest unset, and stop asking.
   Never press for a declined field.
4. Write the answers to `config/profile.local.yaml` using the schema above.
   Confirm back to the user, in a short summary, exactly what was saved.
5. Tell the user the profile is local-only, never committed, and can be
   edited or deleted at any time by asking again or asking to reset it.

## Deleting or resetting a profile

If the user asks to delete or reset their profile, remove or empty
`config/profile.local.yaml` and confirm it was cleared. Do not run the full
interview for a pure delete request.

## Failure behavior

If the file cannot be written (for example, a permissions error), tell the
user plainly and show the values so they can save them manually. Never
invent profile values the user did not provide, and never carry values over
from a different user's session.

## Evaluation cases

- Positive: "Set up a profile for me, I'm a grad student working on
  reproducible genomics pipelines."
- Positive: "Update my profile, I don't want to see anything about clinical
  trial design."
- Negative: "What does The Turing Way say about version control?" (answer
  the question; do not start a profile interview.)
- Negative: "Delete my profile." (clear the file; do not re-run the
  interview.)
