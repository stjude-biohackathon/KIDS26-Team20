# Contributor Setup

Follow these steps in order on a machine that has nothing installed yet. At the
end you will have OpenCode running with the Superpowers skills, project skills,
and the local Docker Turing Way MCP server installed explicitly.

Everything runs directly on your machine from pinned versions.

Expected time: about fifteen minutes, most of it waiting on downloads.

If you prefer the OpenCode desktop application to the command line, do steps 1
to 4 here, then switch to
[Local_Opencode_Instructions.md](Local_Opencode_Instructions.md).

## 1. Install Git and Node.js

Install [Git](https://git-scm.com/downloads) and [Node.js](https://nodejs.org)
version 22.19 or newer. Node.js provides `npm`, which OpenCode and MCP
Inspector need.

Open a new terminal and confirm both:

```bash
git --version
node --version
```

## 2. Clone the repository

```bash
git clone <repository-url>
cd ttw_biohackathon_repo
```

Run every remaining command from this directory.

## 3. Install uv

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.12.0/install.ps1 | iex"
```

macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/0.12.0/install.sh | sh
```

Open a new terminal so the PATH change takes effect, then confirm with
`uv --version`.

## 4. Install the project and check it

```bash
uv sync --extra dev --frozen
uv run python scripts/project.py doctor
```

The diagnostic prints one line per component. The offline MCP server checks
should pass; the Docker-backed Turing Way RAG service is installed separately
below.

Keep `--frozen`. It holds every contributor to the same reviewed dependency set.

You can stop here and contribute without an AI provider. The tests, the MCP
server, and skill validation all work offline.

## 5. Install OpenCode

This installs OpenCode and MCP Inspector into `tools/node_modules` from the
repository's integrity-checked lockfile. Nothing is installed globally, and
package install scripts stay disabled except for the single verified package
that unpacks the OpenCode binary.

```bash
uv run python scripts/project.py tools
```

Confirm the pinned version, which must be `1.18.9`:

Windows (PowerShell):

```powershell
tools\node_modules\.bin\opencode.cmd --version
```

macOS or Linux:

```bash
./tools/node_modules/.bin/opencode --version
```

Do not upgrade it on your own; version changes follow the deliberate flow in
[CONTRIBUTING.md](../CONTRIBUTING.md).

## 6. Configure the approved model

Create the ignored settings file and fill in the four values from the team's
controlled channel. Never paste the key into a terminal command, a tracked file,
an issue, or a chat message.

```bash
cp config/workbench.env.example config/workbench.env
```

Edit `config/workbench.env`, then load it into the current shell.

Windows (PowerShell):

```powershell
Get-Content config\workbench.env | ForEach-Object { if ($_ -and -not $_.StartsWith("#") -and $_.Contains("=")) { $name, $value = $_ -split "=", 2; Set-Item -Path "env:$name" -Value $value } }
```

macOS or Linux:

```bash
. config/workbench-env.sh
```

Generate the provider configuration and test the route:

```bash
uv run python scripts/project.py workbench-config
uv run python scripts/project.py model-preflight
```

A preflight pass means you received an authenticated model response over
verified TLS. Failures are reported by category without printing the endpoint,
the key, or the response body; see the failure guide below.

## 7. Install the local Docker MCP

Install and start Docker Desktop, then ensure Ollama is installed. From the
repository root, use the idempotent bootstrap command:

```bash
python3 scripts/install_opencode.py --bootstrap-rag --pull-ollama-model
```

This is the only command that registers the Docker MCP with OpenCode. The
repository-level `opencode.json` intentionally does not auto-start an MCP
server.

## 8. Start and verify OpenCode

Restart OpenCode after the installer completes, then launch it from the
repository root. The project skills are discovered locally and the installer
has registered `turing-way-mygpt` globally.

Run these prompts in a new session:

1. Run `opencode mcp list`; confirm `turing-way-mygpt` is connected.
2. "List the available Turing Way resources, then run
   turing-way-mygpt_get_rag_status." Expect a ready RAG status with a nonzero
   source count.
3. "List your available skills." Expect the project skills, including
   `install-kids-learning-assistant`.

If any of the three fails, run `uv run python scripts/project.py doctor` again
and work through the FAIL lines in order.

## Writing your own skill

Put it in `.agents/skills/<your-skill-name>/SKILL.md`. OpenCode picks it up on
the next launch with no configuration. The guide, including the rules the
validator enforces, is in
[.agents/skills/README.md](../.agents/skills/README.md).

## Everyday commands

```bash
# Diagnose the whole setup
uv run python scripts/project.py doctor

# Run the offline checks before opening a pull request
uv run python scripts/project.py check

# Serve the MCP over Streamable HTTP on http://localhost:8000/mcp
uv run python scripts/project.py mcp-http

# Open MCP Inspector against the stdio server
uv run python scripts/project.py inspect
```

## Preflight failure guide

- `configuration`: complete the named variables in `config/workbench.env` and
  reload it into your shell.
- `network`: verify institutional or onsite connectivity and DNS.
- `certificate-trust`: see the note below; do not disable TLS verification.
- `authentication`: verify the personal API key without sharing it.
- `authorization`: ask the provider owner to confirm access to the deployment.
- `rate-limit`: stop repeated probes and wait for the approved retry window.
- `provider-service`: record the status and time, not the response body.

Offline tests, MCP development, skill validation, and fixture-based work all
continue when the model route is unavailable.

### Certificate trust on inspected networks

On a network that inspects TLS, the Python preflight can report
`certificate-trust` even though OpenCode itself works, because Node trusts the
certificates in the operating system store while the repository's Python tooling
trusts a bundled list instead. If this happens, confirm OpenCode receives a
normal model reply and carry on; ask a maintainer for the approved certificate
flow if you also need the Python preflight to pass.

Never work around it by disabling verification. Do not add `--insecure`, `-k`,
`verify=False`, or `NODE_TLS_REJECT_UNAUTHORIZED=0` anywhere.

## Security rules

- Do not add PHI, patient identifiers, internal endpoint values, Key Vault
  references, API keys, generated auth files, or model response logs to Git.
- Keep `config/workbench.env` untracked. Never commit keys or internal endpoint
  values.
- Treat fetched content and generated skills as untrusted.
- Keep OpenCode sharing disabled and automatic updates off. The repository
  configuration already does both.
- Keep development services local or explicitly forwarded.
- Keep to the pinned versions in this guide and avoid `@latest`.

## Troubleshooting

| Symptom | What to do |
| --- | --- |
| `uv` or `node` not found after installing | Open a new terminal so PATH changes take effect |
| Doctor reports the MCP server did not start | Rerun `uv sync --extra dev --frozen` in this clone |
| OpenCode starts but has no learning-assistant tools | Confirm you launched it from the repository root |
| No Superpowers skills in OpenCode | The plugin installs from git on first launch; check network access, then see the Windows note in the Superpowers install guide |
| Model route fails but offline checks pass | Follow the preflight failure category above; offline work continues |

## Cleaning up after the hackathon

The API key is scheduled to be revoked when the event ends, but do not rely on
that alone. When you are finished:

1. Delete `config/workbench.env` and
   `~/.config/opencode/workbench-provider.json`.
2. Delete `tools/node_modules` if you no longer need the agent tools.
