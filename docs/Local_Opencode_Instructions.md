# Restricting Local OpenCode Desktop to the Approved Kimi Model

## Scope

This guide is for a person setting up the **OpenCode desktop application** on their own Windows machine so that it offers exactly one model: the approved Kimi K3 deployment behind the team gateway.

Out of the box, OpenCode lists hundreds of models from dozens of providers, including free tiers the team does not own and has not approved. Nothing is wrong with your install when you see that list; OpenCode ships a catalogue of every provider it knows about. This guide replaces that catalogue with a single approved route.

Read this alongside [SETUP.md](SETUP.md), which describes the command-line path and the project checks. The desktop application and the command-line OpenCode from SETUP.md are both supported; complete steps 1 and 2 of SETUP.md either way, so the offline MCP, tests, and skills work in your clone.

Expected time: about fifteen minutes.

## What you will end up with

- One provider, named `aimaas`, pointing at the approved gateway.
- One model, shown in the picker as `Kimi K3 (approved)`.
- Every other provider suppressed, so the picker cannot offer an unapproved model.
- Automatic updates and session sharing both switched off.

## Prerequisites

- OpenCode desktop installed and launched at least once, so that its configuration directory exists.
- The four approved values from the team's controlled channel: the base URL, the model name, the API key, and the API key header name.
- A text editor.

Never paste the API key into a chat message, an issue, a commit, or a terminal command that will be saved in shell history.

## 1. Find the file you need to edit

OpenCode desktop reads a single user-level configuration file. On Windows it lives here:

```text
C:\Users\<you>\.config\opencode\opencode.jsonc
```

The same directory holds OpenCode's own housekeeping files; leave those alone. If `opencode.jsonc` contains only a `$schema` line, that is the default state and it is safe to replace the whole file.

This path is deliberately outside the repository. Do not move this file into the repository and do not commit it, because it will contain your API key.

## 2. Work out the model name the gateway actually wants

This is the step that most often goes wrong, so do it before you write any configuration.

The gateway is an Azure API Management endpoint. Your base URL looks like this:

```text
https://<gateway-host>/<deployment-name>/openai/v1
```

The gateway routes on the **deployment name**, which is the first path segment of your base URL. It does **not** route on the friendly catalogue name that the team may have circulated, which is typically a readable label of the form `<Prefix>-<Model>-<Version>`.

Sending the catalogue name produces a confusing error that looks like the model is missing entirely:

```json
{ "error": { "code": "DeploymentNotFound", "message": "The API deployment for this resource does not exist." } }
```

So read your base URL, take the path segment immediately after the host, and write it down. That string is what you will use as the model id in step 3. You can confirm you have the right one at the end of step 6, where a successful response echoes an upstream name containing `kimi-k3`.

## 3. Write the configuration

Open `opencode.jsonc` in your editor, delete everything in it, and paste the following. Then replace each `<...>` placeholder with your own approved value.

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "autoupdate": false,
  "share": "disabled",
  "provider": {
    "aimaas": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Approved Kimi provider",
      "options": {
        "baseURL": "<your approved base URL, no trailing slash>",
        "headers": {
          "<your approved header name>": "<your approved API key>"
        },
        "timeout": 300000,
        "chunkTimeout": 30000
      },
      "models": {
        "<the deployment name from step 2>": {
          "name": "Kimi K3 (approved)",
          "tool_call": true
        }
      }
    }
  },
  "model": "aimaas/<the deployment name from step 2>",
  "small_model": "aimaas/<the deployment name from step 2>",
  "disabled_providers": [
    "opencode",
    "github-copilot",
    "github-models",
    "anthropic",
    "openai",
    "google",
    "google-vertex",
    "openrouter",
    "ollama",
    "lmstudio",
    "groq",
    "mistral",
    "deepseek",
    "xai",
    "cerebras",
    "togetherai",
    "amazon-bedrock",
    "azure",
    "zhipuai",
    "moonshotai",
    "huggingface",
    "vercel",
    "requesty",
    "perplexity",
    "fireworks-ai"
  ]
}
```

Five details are worth understanding rather than copying blindly:

- The `npm` value must be the **bare package name, with no version suffix**. The desktop application ships this driver built in and finds it by matching that string exactly; writing `@ai-sdk/openai-compatible@3.0.15` misses the built-in copy and sends the app hunting for a package it cannot install, which surfaces as `Failed to initialize provider: aimaas`. (The command-line OpenCode in [SETUP.md](SETUP.md) is different: it installs the driver from the registry, so there the version pin is correct and deliberate.)
- The key inside `models` is sent to the gateway verbatim as the `model` field. The `name` beside it is only a label for the picker, which is why the picker can read `Kimi K3 (approved)` while the request carries the deployment name.
- `model` sets the default for new sessions. `small_model` covers the cheap internal calls OpenCode makes for things like title generation; pointing it at the same model stops OpenCode reaching for a provider you do not own.
- `disabled_providers` is what empties the picker. Every entry is a provider id OpenCode would otherwise advertise.
- `autoupdate` is off to match the version pinning the repository relies on. Do not turn it on.

Save the file. It must be valid JSON with no trailing commas; OpenCode will refuse to start otherwise.

## 4. Restrict who can read the file

The file now contains a live credential, so remove inherited permissions and grant access only to yourself. Run this in PowerShell:

```powershell
icacls "$env:USERPROFILE\.config\opencode\opencode.jsonc" /inheritance:r /grant:r "${env:USERNAME}:(F)"
```

This is a reasonable precaution rather than strong protection. The key is still readable by anything running as you. Treat it as a short-lived hackathon credential, not a durable secret.

## 5. Restart OpenCode

Fully quit the desktop application and start it again. Configuration is read at startup, so an already-running instance will keep the old model list.

## 6. Confirm the result

Two checks. Both should pass.

**The picker offers one model.** Open the model selector in the desktop application. You should see a single provider, `Approved Kimi provider`, containing a single entry, `Kimi K3 (approved)`. If you still see a long list of other providers, your file did not parse or the application did not restart.

**The route works.** Start a new session and send a short prompt, such as `Reply with only the word ready.` A normal reply means the base URL, header name, key, and deployment name are all correct.

If you want to confirm the model identity precisely, the gateway's response reports an upstream name containing `kimi-k3`. That is the same model regardless of the local label.

## Why the free models disappear

Worth knowing so the behaviour is not mysterious later.

OpenCode builds its model list from two sources: the public [models.dev](https://models.dev) catalogue, which is bundled with the application and lists providers whether or not you have credentials for them, and any provider you define yourself. Defining the `aimaas` provider adds your approved route. Listing the others in `disabled_providers` hides the catalogue entries. Neither action deletes anything from your machine, and removing the `disabled_providers` block brings the full list straight back.

## Security rules

The rules in [SETUP.md](SETUP.md) apply unchanged. In particular:

- Keep the configuration file out of the repository and out of version control.
- Never commit the API key, the gateway host, or the deployment name.
- Never disable TLS verification. Do not add `--insecure`, `-k`, `verify=False`, or `NODE_TLS_REJECT_UNAUTHORIZED=0` anywhere. If TLS fails, ask a maintainer for the approved certificate flow.

## Troubleshooting

| Symptom | Cause | What to do |
| --- | --- | --- |
| Picker still lists many providers | File did not parse, or the app was not restarted | Validate the JSON, then fully quit and relaunch |
| Picker is empty | `model` does not match a key under `models` | Make the two deployment-name strings identical |
| `Failed to initialize provider: aimaas` | `npm` field carries a version suffix, so the built-in driver is not matched | Use the bare name `@ai-sdk/openai-compatible`, then fully restart |
| `DeploymentNotFound`, HTTP 404 | You used the catalogue name instead of the deployment name | Redo step 2 |
| `Missed model deployment`, HTTP 400 | The `model` field reached the gateway empty | Check the `models` key is a non-empty string |
| HTTP 401 | Key or header name wrong | Re-copy both from the controlled channel; the header name is not `Authorization` |
| HTTP 429 | Shared rate limit | Wait and retry; do not add a second provider to work around it |
| OpenCode starts but no MCP tools | Unrelated to this guide | See [SETUP.md](SETUP.md) |

### If the command-line preflight fails while the desktop app works

This combination is expected on a network that inspects TLS, and it is not a fault in your setup.

The desktop application runs on Node 24, which trusts the certificates in the Windows certificate store, so an inspected connection succeeds. The repository's Python tooling trusts a bundled list instead, which does not include a corporate or Cloudflare Gateway inspection root. That is why `uv run python scripts/project.py model-preflight` can report `certificate-trust` on a machine where the desktop application is working normally.

Nothing in this guide depends on fixing that. Ask a maintainer for the approved certificate flow if you also need the command-line preflight to pass, and verify the certificate fingerprint against the team's approved value before trusting it. Do not work around it by disabling verification.

## Cleaning up after the hackathon

The API key is scheduled to be revoked when the event ends, but do not rely on that alone. When you are finished:

1. Delete `C:\Users\<you>\.config\opencode\opencode.jsonc`, or at minimum remove the `headers` block containing the key.
2. Uninstall OpenCode desktop if you installed it only for the event.
3. Delete any local copy of the certificate or environment file you created along the way.
