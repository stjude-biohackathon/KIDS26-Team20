---
name: path-formatter
description: Builds a correctly formatted Turing Way "pathway" block from a list of content (chapters, sections, or topics), producing valid MyST {curation} directive markup - title, description, label, and a nested item/children list - ready to drop into a pathway page. Use this whenever the user provides a list of chapters or resources and asks to build, format, or assemble a pathway, curated list, or "path" through the book, or asks how to turn a list of content into Turing Way's pathway format - even if they don't say "curation directive" explicitly.
license: MIT
compatibility: opencode, claude-code, github-copilot
metadata:
  audience: contributors
  status: draft
---

# Path Formatter

## Use this skill when

The user has an ordered or unordered list of Turing Way chapters, resources,
or sections (or a manifest-style list, e.g. from `ttw_manifest.yaml`) and
wants it turned into a formatted pathway / curation block. Trigger on
requests like "build a path from these chapters," "turn this list into a
curation directive," "format this as a Turing Way pathway," or "how do I
nest a sub-section under a chapter here."

## Do not use this skill when

- The user wants help deciding *which* chapters belong in a pathway. That is
  a curation/content judgment call, not a formatting task - point them to
  the persona or resource-curation workflow instead.
- The request is for general markdown formatting unrelated to Turing Way's
  pathway syntax (e.g. "make this a bullet list for my README").

## Required tools

This is primarily a text-transformation task and may need no tools at all if
the user supplies exact file paths or anchors directly. If the input
references chapters by name or topic rather than an exact path, use:

- `learning-assistant_list_resources` - resolve a human-readable chapter or
  topic name to its real file path (and any relevant heading anchors),
  rather than guessing or inventing one.
- `learning-assistant_get_resource` - confirm a chapter's actual heading
  anchors when the user wants to nest a specific section rather than link
  the whole chapter.

## Workflow

1. Get the list of content to include, and any intended grouping (e.g. a
   specific section nested under its parent chapter via `children`).
2. Resolve each entry to a valid `item` reference:
   - A relative file path for a full chapter. Real Turing Way pathways live
     in `book/website/pathways/` and reference chapters relative to that
     directory, for example `../reproducible-research/vcs.md` or
     `../collaboration/github-novice.md` - keep the `../` and match this
     convention rather than inventing a bare or absolute path.
   - A heading anchor (e.g. `#section-anchor`) for a specific section nested
     under an already-referenced chapter. **Quote it** as `'#section-anchor'`:
     an unquoted `#` starts a YAML comment, which silently drops the rest of
     the line instead of producing an error.
   If the exact path or anchor isn't already known, look it up rather than
   inventing one; if no lookup tool is available, ask the user to confirm it.
3. Determine the title, a one-to-two sentence `description` (Markdown is
   allowed and is processed by MyST), and a `label` slug following the real
   convention seen in every existing pathway: `pathway-<slug>` (for example
   `pathway-early-career-researchers`), not a `cur-` prefix. This `label` is
   the curation block's own identifier and is distinct from the pathway
   page's top-level heading anchor (`(pw-<slug>)=`), which this skill does
   not generate - it produces the block to drop beneath an existing page
   heading, not the page itself.
4. Assemble the block in the exact MyST curation syntax:

   ```markdown
   :::{curation} <Title>
   ---
   depth: 2
   description: >
     <one-to-two sentence description>
   label: pathway-<slug>
   ---
   - item: <path-or-anchor>
     children:
       - item: <path-or-anchor>
   - item: <path-or-anchor>
   :::
   ```

   `depth: 2` is what every existing Turing Way pathway file uses; only
   change it if the user has a specific reason to nest more shallowly or
   deeply.

5. If the list exceeds roughly 15 top-level items, flag this to the user -
   Turing Way's own pathway-creation guidance recommends "a maximum of
   around 15 chapters to maintain focus" - and ask whether to prioritize
   rather than silently truncating.
6. Present the finished block for the user to paste into the relevant
   pathway file, or write it directly if operating with file access.

## Failure behavior

If an item can't be resolved to a real path or anchor, do not fabricate one.
List it separately as "unresolved" and ask the user to confirm the correct
target. If the list has no clear order or grouping, ask rather than guessing
at structure.

## Evaluation cases

- Positive: "Here's my list of 8 chapters for the trainee persona - format
  this into a pathway block" (with the list attached).
- Positive: "How do I nest a specific section under a chapter in a Turing
  Way pathway?"
- Negative: "Which chapters should I include for a wet-lab biologist?"
  (curation judgment, not formatting.)
- Negative: "Format this as a numbered list for my README." (general
  markdown, unrelated to Turing Way's pathway syntax.)
