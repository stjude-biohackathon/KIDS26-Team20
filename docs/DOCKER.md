# Local Docker MCP server

Run the learning-assistant MCP server locally without installing Python, `uv`,
or Node.js. Install and start [Docker Desktop](https://docs.docker.com/get-docker/)
for macOS, Windows, or Linux first. Docker Desktop is intentionally not
installed by this project because it is operating-system software that may
require administrator approval and a user license/sign-in decision.

For a first install or repair, run the idempotent bootstrap command:

```bash
python3 scripts/install_opencode.py --bootstrap-rag --pull-ollama-model
```

It reconciles the managed OpenCode configuration and skill symlinks, reuses
existing MyGPT secrets and Docker volumes, starts the stack, waits for its
services to become healthy, and initializes the corpus only when the dataset
passes its compatibility checks. The explicit `--pull-ollama-model` flag
downloads `nomic-embed-text` only if absent. It does not delete Docker volumes or
overwrite a non-symlink skill directory. To configure OpenCode without
starting the stack, run `python3 scripts/install_opencode.py`.

The server is available only on the same computer at
`http://127.0.0.1:8000/mcp`. It retrieves the full Turing Way corpus from its
pinned GitHub commit by default, so recommendations and repository reviews can
be grounded in the relevant source rather than a small starter sample. If
GitHub is unavailable, it automatically falls back to the committed snapshot
and returns `origin: "snapshot"` for that evidence. Confirm the process is
healthy at `http://127.0.0.1:8000/health`. Stop it with `docker compose down`.

`scripts/install_opencode.py` creates `config/mygpt.env` with unique local
database and Django secrets when it does not exist, creates global OpenCode
skill links that point back to this repository's canonical `.agents/skills`
definitions, adds the local MCP endpoint to `~/.config/opencode/opencode.json`,
deduplicates its managed instruction path, and preserves unrelated OpenCode
settings. It first checks that Docker Desktop is installed and its daemon is
running, then reports the Docker installation link if it is not. Restart
OpenCode after running it.

To use a different unused local port, set `LEARNING_ASSISTANT_HOST_PORT` before
starting Compose:

```bash
LEARNING_ASSISTANT_HOST_PORT=8080 docker compose up --build
```

MyGPT's library API is also available only on the same computer at
`http://127.0.0.1:8001`. Use this direct endpoint for local MyGPT API requests.
To select a different unused host port, set `MYGPT_BACKEND_HOST_PORT` before
starting Compose:

```bash
MYGPT_BACKEND_HOST_PORT=8002 docker compose up --build
```

## Connect an MCP client

Configure a client that supports Streamable HTTP MCP with this URL:

```text
http://127.0.0.1:8000/mcp
```

Use `list_resources` to discover source IDs, then `get_resource` to read a
chapter. Resource discovery does not call a model; the separate MyGPT tools
perform the retrieval queries described below. Start discovery with
`{"limit": 200, "offset": 0}` and advance
`offset` by the number of entries returned until the needed chapters are
found or a page contains fewer than 200 entries.

After a server-tool change, rebuild and recreate only the MCP service from
the configured deployment checkout:

```bash
docker compose up --detach --build --no-deps --wait learning-assistant
```

This does not rebuild MyGPT or change its data volumes. Reconnect the MCP
client so it discovers the updated tool schema; a client still advertising
only `limit` cannot request later pages.

The default tests remain offline. To explicitly verify the running server's
pagination, all healthcheck chapter reads, and MyGPT evidence retrieval, run
this optional live check in PowerShell:

```powershell
$env:LEARNING_ASSISTANT_LIVE_MCP_URL = "http://127.0.0.1:8000/mcp"
try {
    uv run python -m pytest tests\test_live_mcp_pagination.py -m integration -s
} finally {
    Remove-Item Env:\LEARNING_ASSISTANT_LIVE_MCP_URL
}
```

This check performs read-only calls to the configured MCP server, GitHub,
and MyGPT; it does not write a repository score report.

## MyGPT and skills

Compose builds MyGPT's backend Dockerfile from the pinned upstream commit,
starts PostgreSQL, exposes MyGPT's API only on the Docker host loopback at
`http://127.0.0.1:8001`, and connects the MCP server to
`http://mygpt-backend:8000` over its private Docker network. The optional
`mygpt-library` skill calls the documented read-only MyGPT API to list the
caller's datasets and document titles, and to retrieve cited context from a
selected dataset. `query_mygpt_context` calls MyGPT's `/api/get_context/`
endpoint and preserves its source records in the typed MCP response.

[`config/mygpt-bootstrap.yaml`](../config/mygpt-bootstrap.yaml) is the tracked
source of truth for the MyGPT Turing Way dataset. It records the dataset name
(`turing-way`), pinned source revision and expected document count, chat model
(`qwen2.5:3b`), embedding model (`nomic-embed-text` from Ollama), chunking, and
retrieval settings. It does not contain model weights, a generated vector
index, credentials, or scientific data.

Before question retrieval can return Turing Way evidence, initialize MyGPT
using those settings, import the full pinned corpus, and build its embeddings.
By default, MyGPT calls the Ollama server already running on the Docker host at
`http://host.docker.internal:11434`, using `nomic-embed-text` for embeddings.
The retrieval API records `qwen2.5:3b` as its MyGPT model type but does not
require its local Ollama weights. Install the embedding model before bootstrap:

```bash
ollama pull nomic-embed-text
```

Set `MYGPT_OLLAMA_URL` or `MYGPT_MODEL_ID` when using a different host service
or chat model.

MyGPT's dataset upload and indexing process is responsible for creating that
dataset. The MCP container does not upload documents or expose another user's
library.

To initialize the local MyGPT dataset from the full pinned Turing Way source,
run this once after the services are healthy:

```bash
docker compose --profile bootstrap run --rm mygpt-bootstrap
```

The bootstrap downloads the configured embedding model and source pages, so it
can take several minutes. On later runs it uses MyGPT's documented
`get_datasets`, `get_dataset_details`, `get_documents`, and `get_context` APIs
to skip only a dataset whose settings, complete source-path title list, nonzero
index, and live retrieval all match the tracked provenance. If any check fails,
it stops without uploading, overwriting, deleting, or rebuilding the existing
dataset. There is intentionally no reset mode: MyGPT's delete-and-upload APIs
are not transactional, so an automated reset could destroy a usable local
dataset. Its data and Chroma index persist in Docker volumes; they are never
committed to this repository.

## Offline development and tests

The committed snapshot exists for deterministic tests and offline development.
To force the container to use only that snapshot, override the Compose
environment setting:

```bash
LEARNING_ASSISTANT_OFFLINE=true docker compose up --detach --build
```

Do not put an API key, internal endpoint, clinical data, or a provider
configuration in Compose files, Docker build arguments, or container
environment variables.
