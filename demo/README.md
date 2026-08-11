# Learner-facing demo

The MCP service runs independently of the learner-facing UI. That UI is the next
P0 deliverable and must consume the server's Streamable HTTP endpoint at
`/mcp` rather than reaching into the retrieval code directly.

## Required first-screen experience

Build the usable learning assistant, not a marketing landing page. The first
screen should provide:

- a compact persona selector;
- an experience-level control;
- suggested learning questions;
- a conversational input;
- source citations that distinguish The Turing Way from institutional sources;
- an ordered learning-path view; and
- visible empty, loading, error, and offline-fixture states.

The interface should be accessible to non-computational staff: restrained
terminology, readable source labels, keyboard navigation, and no unexplained
developer controls.

## Demonstration script

1. Choose **Wet-lab biologist** and **Beginner**.
2. Ask how to make a first computational analysis reproducible.
3. Show cited resources and open one source.
4. Generate an ordered learning path.
5. Switch to the retroactive-best-practices workflow for an example repository.
6. Show that the same MCP and skills are available to a coding client.

## Promotion gate

A replacement UI becomes the primary demo only after the complete script passes
with the offline fixture corpus. Until then, maintain a separately configured
LibreChat fallback. Do not copy personal AI Hub credentials, paths, proxies, or
model configuration into this repository.
