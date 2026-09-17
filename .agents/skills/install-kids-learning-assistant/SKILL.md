---
name: install-kids-learning-assistant
description: Install the KIDS learning assistant's local Docker MCP server and canonical OpenCode skills for a scientist or contributor
license: MIT
compatibility: opencode
metadata:
  audience: scientists-and-contributors
  status: active
---

# Install KIDS Learning Assistant

## Use this skill when

A user asks to install, configure, repair, or verify the KIDS Turing Way and
MyGPT learning assistant in their local OpenCode environment.

## Do not use this skill when

The user asks to deploy the service to a shared server, alter MyGPT data,
configure institutional credentials, or run containers against patient data.

## Workflow

1. Confirm Docker Desktop, OpenCode, and the required host Ollama model
   `qwen2.5:3b` are installed and running. If Docker is
   absent or stopped, direct the user to
   `https://docs.docker.com/get-docker/`; do not silently install system
   software, download a large model, or request credentials.
2. From the KIDS repository root, run:

   ```bash
   python3 scripts/install_opencode.py
   docker compose up --detach --build
   ```

3. For a complete local Turing Way RAG setup, run:

   ```bash
   python3 scripts/install_opencode.py --bootstrap-rag
   ```

4. Restart OpenCode so it discovers the linked global skills and the
   `turing-way-mygpt` MCP server.
5. Run `opencode mcp list` and confirm `turing-way-mygpt` is connected.
6. Test the Turing Way path with `turing-way-mygpt_list_resources` before
   testing any MyGPT-backed query.
7. Run `turing-way-mygpt_get_rag_status`. Treat the RAG pipeline as ready only
   when it returns `status: ready` with a nonzero `source_count`.

## Failure behavior

If Docker is unavailable, say that Docker Desktop must be started. If OpenCode
is unavailable, explain that the MCP and skills will be registered when it is
installed. Do not overwrite a non-symlink skill directory, expose local
configuration values, or claim that MyGPT retrieval works before its dataset is
initialized.

## Evaluation cases

- Positive: a scientist asks for a one-command-style local setup for the KIDS
  Turing Way assistant.
- Positive: a contributor asks why OpenCode cannot discover the review skill.
- Negative: a user asks to deploy the stack to a shared production service.
- Negative: a user asks to add institutional credentials to Compose.
