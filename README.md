# St. Jude AI and Data Learning Assistant

A role-aware learning assistant grounded in The Turing Way and approved St. Jude
educational resources, built for KIDS Biohackathon 2026.

> **Team leads:** Start with the [team lead checklist](project-management/CHECKLIST.md) before the event or during your first team meeting.

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
- **Communication:** [Add the agreed channel or contact]

## Vision and Mission

- **Vision:** Someone at St. Jude with a practical question about reproducible or data-intensive research can get an answer pitched at their level, with citations they can check, drawn only from sources the institution has approved.
- **Mission:** During the biohackathon, build and evaluate the retrieval layer, the MCP tool contract, and the skills that sit on top of them, and demonstrate the whole path end to end with honest limitations.

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

Deliberately very little. It provides two tools:

- `list_resources` — what Turing Way pages are available, each tagged with an
  `origin` of `github` or `snapshot`
- `get_resource` — the full text of one page, by the identifier `list_resources`
  returned

That is enough to prove on day one that the server is installed and that it can
reach GitHub. Everything interesting — ranking, personas, learning paths,
evaluation — is work for the event, not inherited code.

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

MIT. See [LICENSE.md](LICENSE.md).
