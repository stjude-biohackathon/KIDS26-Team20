# Start here

## Set up the contributor environment

The supported environment runs directly on Windows, macOS, or Linux with pinned tools.

1. Install Git and Node.js 22.19 or newer.
2. Follow [docs/SETUP.md](docs/SETUP.md) from top to bottom. It takes a machine with nothing installed to OpenCode running with the Superpowers skills, the project skills, and the Turing Way MCP server started on launch.
3. If you prefer the OpenCode desktop application to the command line, also follow [docs/Local_Opencode_Instructions.md](docs/Local_Opencode_Instructions.md).

You can contribute without an AI provider: the offline tests, MCP development, skill validation, and fixture-based work all run before any model route is configured.

## Verify your environment

```bash
uv run python scripts/project.py doctor
```

The diagnostic reports one line per component — the MCP server, the skills, the
OpenCode install, and the model route — with the next action for anything that
is not ready.

## Common workflows

```bash
# Run Streamable HTTP MCP on http://localhost:8000/mcp
uv run python scripts/project.py mcp-http

# Open MCP Inspector against the stdio server
uv run python scripts/project.py inspect
```

## Write a skill

Skills go in `.agents/skills/<your-skill-name>/SKILL.md`, one level deep.
OpenCode loads that directory automatically, so there is nothing to configure.
Start from [.agents/skills/README.md](.agents/skills/README.md).

Choose a contribution track in `CONTRIBUTING.md`. Ask a maintainer before
adding institutional content or changing deployment boundaries.
