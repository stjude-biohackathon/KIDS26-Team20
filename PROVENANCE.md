# Provenance

## The Turing Way MCP seed

The initial retrieval and MCP design was informed by code in:

- Repository: `https://github.com/the-turing-way/the-turing-way`
- Path: `tools/ttw-ai-server`
- Source commit: `6835ae2908ea44178c741d5be9c1a8fe35fb226d`
- Commit date: 2026-05-27
- License declared by the seed package: MIT

This repository rewrites the transport layer for the official MCP Python SDK v2
and generalizes the content source rather than copying the original files
verbatim. The snapshot text under `corpus/fixtures/turing-way` is short,
purpose-written test material derived from general concepts in The Turing Way.
The complete Turing Way book remains CC BY 4.0 and should be cited when used.

## CMPB AI Hub

The separation between a portable contributor workbench and a learner-facing
demo was developed in `cmpb_ai_hub/docs/HACKATHON_IMPLEMENTATION_PLAN.md`. No
machine-specific credentials, certificates, model files, or registry settings
were copied from that deployment.
