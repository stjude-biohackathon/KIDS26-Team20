# St. Jude AI and Data Learning Assistant

A role-aware learning assistant grounded in The Turing Way and approved St. Jude
educational resources, built for KIDS Biohackathon 2026.

Onboarding:
> **Project leads:** Start with the [team lead checklist](project-management/CHECKLIST.md) before the event or during your first team meeting.
> **Everyone else:** Start with [START_HERE.md](START_HERE.md). It takes a machine
> with nothing installed to a working environment in about fifteen minutes.

## Project Profile

- **Project name:** St. Jude AI and Data Learning Assistant
- **Question, problem, or opportunity:** People across St. Jude need practical guidance on reproducible research, data handling, and AI tooling, but that guidance is scattered and often written for an audience that already knows the vocabulary. Can an assistant give role-appropriate, properly cited answers drawn only from approved sources?
- **Data, inputs, or evidence:** [The Turing Way](https://the-turing-way.start.inria.fr/) (CC-BY-4.0), pinned to a specific commit and included as an offline snapshot so the project works without network access. Approved St. Jude learning resources are configured but disabled pending ownership, scope, and licence review.
- **Expected output:** An MCP server exposing typed, citation-preserving tools; a set of Agent Skills that use it; deterministic evaluations; and a demonstration that a non-specialist can follow.
- **Tools and stack:** Python 3.12, uv, the official MCP Python SDK v2 (stdio and Streamable HTTP), the GitHub API, pytest, ruff, and OpenCode as the agent interface. Retrieval approach is an open decision for the team.
- **Team lead:** [Name and GitHub handle]
- **Team members and roles:** See [project-management/team.md](project-management/team.md)
- **Communication:** [Slack-Team20](https://stjudebiohackathon.slack.com/archives/C0BRYK69JBH)

## Vision and Mission

- **Vision:** Create a helpful AI assistant that tailors its responses to practical questions about reproducible or data-intensive research for users at different levels (novice, advanced, or a specific profile), with citations they can check, drawn only from sources the institution has approved.
- **Mission:** Build and evaluate the retrieval layer, the MCP tool contract, and the skills that sit on top of them, and demonstrate the whole path end to end with honest limitations. Plan a future development scope to make these assistants to help with domain-specific questions.

## Contributors and Team Members

- Ty Michael
- Saikat Nandy
- Chris House
- Arif Usta
- Jaimin Patel
- Chen Li
- Shovito Barua Soumma
- Aliyah Cole

**For any questions, please contact:** ty.michael@stjude.org, jaimin.patel@stjude.org and malvika.sharan@stjude.org.

## About

Research guidance fails people in two directions at once. Written for specialists, it assumes vocabulary that a wet-lab biologist or a new trainee does not have. Written for beginners, it is too shallow to act on. The gap is widest exactly where reproducibility matters most.

A general-purpose chatbot is a poor fix, because it cannot say where an answer came from and will invent a plausible citation when it does not know. This project takes the opposite approach: every answer carries its source, and the assistant is restricted to a reviewed corpus. When it cannot answer from that corpus, it says so.

The Turing Way is the starting corpus because it is openly licensed, community reviewed, and covers the ground the audience needs. Institutional sources are kept behind an explicit approval gate rather than added by default.

## Getting Started

```bash
uv sync --extra dev --frozen
uv run python scripts/project.py doctor
```

The diagnostic prints one line per component with the next action for anything
not ready. Full instructions, from installing Git through a verified OpenCode
session, are in [docs/SETUP.md](docs/SETUP.md).

You can contribute without an AI provider. The tests, the MCP server, and skill
validation all work offline.

### Run locally with Docker

For the easiest scientist-facing setup, install and start
[Docker Desktop](https://docs.docker.com/get-docker/) for your operating
system. Docker Desktop is a user-approved system installation and is not
installed automatically. For a first install or repair, run this idempotent
bootstrap command:

```bash
python3 scripts/install_opencode.py --bootstrap-rag --pull-ollama-model
```

The installer checks Docker Desktop and the required host Ollama models
(`qwen2.5:3b` and `nomic-embed-text`) before changing any configuration. It reconciles the managed
OpenCode MCP entry and canonical skill symlinks, reuses existing MyGPT settings
and Docker volumes, then waits for the local services to become healthy before
initializing the full Turing Way RAG corpus. The explicit
`--pull-ollama-model` flag authorizes downloading either required model only
when absent; it is a no-op when both models are already installed. The installer never
deletes Docker volumes or replaces a non-symlink skill directory. To register
OpenCode configuration without starting Docker or initializing RAG, use:

```bash
python3 scripts/install_opencode.py
```

For a clean OpenCode-only reinstall, preserving Docker containers, volumes, and
MyGPT settings, run:

```bash
python3 scripts/install_opencode.py --uninstall
```

The installer registers `turing-way-mygpt` in global OpenCode configuration and
links the canonical skills from this repository into OpenCode's global skill
directory without copying them. The Compose command starts the local stack,
retrieves the full pinned Turing Way corpus, and exposes Streamable HTTP MCP at
`http://127.0.0.1:8000/mcp` and MyGPT's library API at
`http://127.0.0.1:8001`. It automatically falls back to the committed
snapshot if GitHub is unavailable. See [the Docker guide](docs/DOCKER.md).

To have OpenCode perform the initial installation from this repository, use
this exact prompt:

```text
Use the install-kids-learning-assistant skill. From this KIDS repository root,
install or reconcile the local KIDS Learning Assistant for OpenCode by running
python3 scripts/install_opencode.py --bootstrap-rag --pull-ollama-model.
Preserve unrelated OpenCode settings; do not replace a non-symlink skill
directory or delete Docker volumes. When it finishes, report the MCP and RAG
readiness and tell me to restart OpenCode.
```

After restarting OpenCode, use `opencode mcp list` and
`turing-way-mygpt_get_rag_status` to confirm the new session sees the MCP and
the indexed corpus.

MyGPT's repeatable Turing Way dataset settings live in
[`config/mygpt-bootstrap.yaml`](config/mygpt-bootstrap.yaml). It specifies the
source manifest and embedding model, but intentionally excludes downloaded
model weights and generated vector indexes. Use `get_rag_status` after
bootstrap to confirm that the configured model can retrieve Turing Way sources.

### Choose a Turing Way path

Ask OpenCode to "help me choose my Turing Way path." The `turing-way-pathfinder`
skill asks only for your current role and immediate goal, then chooses one of
the Turing Way's curated pathways and returns a short, scored, cited checklist.
It does not request research data or personal information.

### Review a research repository

Launch OpenCode from this repository and use the `turing-way-review` skill to
assess a checked-out research software repository against cited Turing Way
guidance. It assigns a transparent rating out of six across project design,
reproducibility, and version-control collaboration, then prioritizes practical
improvements. It is an evidence-based baseline review, not a compliance,
security, or clinical assessment.

## Repository Map

```text
src/learning_assistant/  The MCP server: source loading and two typed tools
.agents/skills/          Agent Skills, including yours. Start with its README
corpus/                  The source manifest and a small offline snapshot
tests/                   Offline test suite, no credentials or network needed
scripts/                 Task runner, diagnostics, and skill validation
docs/                    Setup, project brief, and contributor guides
project-management/      Team plan, roles, and the team lead checklist
```

## What the MCP Server Does Today

The MCP server provides citation-preserving source retrieval plus local MyGPT
RAG evidence:

- `list_resources` — what Turing Way pages are available, each tagged with an
  `origin` of `github` or `snapshot`
- `get_resource` — the full text of one page, by the identifier `list_resources`
  returned
- `get_rag_status` — a live Turing Way retrieval probe for the configured local
  MyGPT model and dataset
- `get_turing_way_evidence_packets` — resolves an exact Turing Way resource ID
  to its pinned citation and performs one matching MyGPT RAG query per final
  recommendation or checklist action
- `get_turing_way_review_evidence` — runs the required broad RAG queries for
  project design, reproducibility, and version control/collaboration

For a repository review, each evidence packet can also carry a separately
observed public GitHub URL for the repository fact. The Turing Way citation
supports the recommendation; the repository URL supports the factual claim
about the reviewed project. MyGPT relevance is a retrieval-match score, not a
scientific-quality or compliance score.

## Roadmap and Milestones

| When | Focus | Expected outcome |
| --- | --- | --- |
| Day 1 | Confirm the question, sources, roles, and environment | Everyone has a working setup and has made one small change |
| Day 2 | Build and compare retrieval, tools, and skills | A measurable result, or clear evidence about what does not work |
| Day 3 | Stabilize, document, and present | A demo with methods, limitations, and next steps |

The goal is not a perfect production system. The goal is a clear, honest, useful result that the team can explain and others can build on.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the tracks, the dependency update
rules, and how to add an MCP tool. To write a skill, see
[.agents/skills/README.md](.agents/skills/README.md).

Run this before opening a pull request:

```bash
uv run python scripts/project.py check
```

## Data and Credentials

**Do not commit passwords, API keys, private information, or identifiable human
or clinical data.** Personal provider settings belong in `config/workbench.env`,
which is ignored by Git and must stay that way. Check the source and licence
before adding external data or media.

Source repository, commit, and licensing metadata are recorded in the manifests
under [`corpus/`](corpus/).

## Licence

MIT License. See [LICENSE.md](LICENSE.md)
