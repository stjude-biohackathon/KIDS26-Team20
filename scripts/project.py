"""Small cross-platform task runner for contributors and CI."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*command: str, env: dict[str, str] | None = None, cwd: Path | None = None) -> None:
    print(f"+ {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=cwd or ROOT, env=env, check=True)


def which(command: str) -> str | None:
    """Resolve a command, preferring the repository's pinned tools directory."""
    search_path = os.pathsep.join(
        [str(ROOT / "tools/node_modules/.bin"), os.environ.get("PATH", "")]
    )
    return shutil.which(command, path=search_path)


def main() -> int:
    task = sys.argv[1] if len(sys.argv) > 1 else "help"
    offline_env = {
        **os.environ,
        "LEARNING_ASSISTANT_OFFLINE": "true",
        "LEARNING_ASSISTANT_SOURCES": str(ROOT / "corpus/sources.yaml"),
    }
    if task == "check":
        run("uv", "run", "ruff", "format", "--check", ".")
        run("uv", "run", "ruff", "check", ".")
        run("uv", "run", "pytest")
        run("uv", "run", "python", "scripts/validate_skills.py")
    elif task == "doctor":
        run("uv", "run", "python", "scripts/doctor.py")
    elif task == "format":
        run("uv", "run", "ruff", "format", ".")
        run("uv", "run", "ruff", "check", "--fix", ".")
    elif task == "mcp-stdio":
        run("uv", "run", "learning-assistant", "stdio", env=offline_env)
    elif task == "mcp-http":
        run(
            "uv",
            "run",
            "learning-assistant",
            "http",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
            env=offline_env,
        )
    elif task == "tools":
        npm = which("npm")
        if npm is None:
            print("npm was not found; install Node.js 22.19 or newer first.", file=sys.stderr)
            return 2
        run(npm, "ci", "--ignore-scripts", cwd=ROOT / "tools")
        # opencode-ai stages its platform binary in its own postinstall script.
        # Run scripts for that single integrity-verified package only.
        run(npm, "rebuild", "opencode-ai", "--ignore-scripts=false", cwd=ROOT / "tools")
    elif task == "inspect":
        inspector = which("mcp-inspector")
        if inspector is None:
            print(
                "MCP Inspector is not installed; run "
                "`uv run python scripts/project.py tools` first.",
                file=sys.stderr,
            )
            return 2
        run(inspector, "uv", "run", "learning-assistant", "stdio", env=offline_env)
    elif task == "workbench-config":
        run("uv", "run", "python", "scripts/workbench.py", "configure-opencode")
    elif task == "model-preflight":
        run("uv", "run", "python", "scripts/workbench.py", "model-preflight")
    elif task == "workbench-check":
        run("uv", "run", "python", "scripts/project.py", "check")
        run("uv", "run", "python", "scripts/workbench.py", "configure-opencode")
        run("uv", "run", "python", "scripts/workbench.py", "model-preflight")
        opencode = which("opencode")
        if opencode is None:
            print(
                "OpenCode was not found; run `uv run python scripts/project.py tools` first.",
                file=sys.stderr,
            )
            return 2
        run(opencode, "--version")
    elif task == "help":
        print(
            "Tasks: check, doctor, format, mcp-stdio, mcp-http, tools, inspect, "
            "workbench-config, model-preflight, workbench-check"
        )
    else:
        print(f"Unknown task: {task}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
