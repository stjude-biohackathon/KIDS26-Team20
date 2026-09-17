"""Install the KIDS learning-assistant MCP server and skills into OpenCode."""

from __future__ import annotations

import argparse
import json
import os
import secrets
import shutil
import subprocess
import sys
import tempfile
from collections.abc import MutableMapping
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SKILLS = (
    "install-kids-learning-assistant",
    "mygpt-library",
    "skill-formatter",
    "skill-maintainer",
    "skill-template",
    "teacher-skill",
    "turing-healthcheck-prototype",
    "turing-way-pathfinder",
    "turing-way-guidance",
    "turing-way-review",
)
DEFAULT_CONFIG = Path.home() / ".config/opencode/opencode.json"
DEFAULT_SKILLS_ROOT = Path.home() / ".config/opencode/skills"
DOCKER_DESKTOP_URL = "https://docs.docker.com/get-docker/"
REQUIRED_OLLAMA_MODELS = ("qwen2.5:3b", "nomic-embed-text")


def _mapping(value: object, name: str) -> MutableMapping[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a JSON object")
    return value


def _deduplicate(values: list[str]) -> list[str]:
    """Return values in their original order, keeping the first occurrence."""
    return list(dict.fromkeys(values))


def _write_opencode_config(config_path: Path, config: MutableMapping[str, object]) -> None:
    """Atomically write private OpenCode configuration."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=config_path.parent,
        prefix=f".{config_path.name}.",
        delete=False,
    ) as temporary:
        temporary.write(json.dumps(config, indent=2) + "\n")
        temporary_path = Path(temporary.name)
    os.chmod(temporary_path, 0o600)
    temporary_path.replace(config_path)


def update_opencode_config(config_path: Path, repository_root: Path) -> None:
    """Add KIDS configuration without overwriting unrelated OpenCode settings."""
    if config_path.exists():
        data = json.loads(config_path.read_text(encoding="utf-8"))
        config = _mapping(data, str(config_path))
    else:
        config = {"$schema": "https://opencode.ai/config.json"}

    instructions = config.setdefault("instructions", [])
    if not isinstance(instructions, list) or not all(
        isinstance(item, str) for item in instructions
    ):
        raise ValueError("instructions must be a JSON array of paths")
    agent_instructions = str(repository_root / "AGENTS.md")
    instructions[:] = _deduplicate([*instructions, agent_instructions])

    permissions = _mapping(config.setdefault("permission", {}), "permission")
    skill_permissions = _mapping(permissions.setdefault("skill", {}), "permission.skill")
    skill_permissions.update(
        {
            "mygpt-library": "allow",
            "turing-way-*": "allow",
        }
    )

    mcp_servers = _mapping(config.setdefault("mcp", {}), "mcp")
    mcp_servers["turing-way-mygpt"] = {
        "type": "remote",
        "url": "http://127.0.0.1:8000/mcp",
        "enabled": True,
        "oauth": False,
        "timeout": 30000,
    }

    _write_opencode_config(config_path, config)


def remove_opencode_config(config_path: Path, repository_root: Path) -> bool:
    """Remove only this repository's managed OpenCode configuration entries."""
    if not config_path.exists():
        return False
    config = _mapping(json.loads(config_path.read_text(encoding="utf-8")), str(config_path))
    changed = False

    instructions = config.get("instructions")
    if instructions is not None:
        if not isinstance(instructions, list) or not all(
            isinstance(item, str) for item in instructions
        ):
            raise ValueError("instructions must be a JSON array of paths")
        managed_instruction = str(repository_root / "AGENTS.md")
        filtered_instructions = [item for item in instructions if item != managed_instruction]
        if filtered_instructions != instructions:
            config["instructions"] = filtered_instructions
            changed = True

    mcp_servers = config.get("mcp")
    if mcp_servers is not None:
        mcp_mapping = _mapping(mcp_servers, "mcp")
        if mcp_mapping.pop("turing-way-mygpt", None) is not None:
            changed = True

    if changed:
        _write_opencode_config(config_path, config)
    return changed


def install_skill_links(skills_root: Path, repository_root: Path) -> None:
    """Link global OpenCode skills to the repository's canonical definitions."""
    skills_root.mkdir(parents=True, exist_ok=True)
    for name in CANONICAL_SKILLS:
        source = repository_root / ".agents/skills" / name
        target = skills_root / name
        if not source.is_dir():
            raise FileNotFoundError(f"canonical skill is missing: {source}")
        if target.exists() and not target.is_symlink():
            raise FileExistsError(f"refusing to replace existing skill directory: {target}")
        target.unlink(missing_ok=True)
        target.symlink_to(source, target_is_directory=True)


def remove_skill_links(skills_root: Path) -> list[Path]:
    """Remove only managed canonical skill symlinks, leaving real directories intact."""
    removed: list[Path] = []
    for name in CANONICAL_SKILLS:
        target = skills_root / name
        if target.is_symlink():
            target.unlink()
            removed.append(target)
    return removed


def create_mygpt_environment(repository_root: Path) -> Path:
    """Create local MyGPT database and Django secrets without overwriting them."""
    environment_path = repository_root / "config/mygpt.env"
    if environment_path.exists():
        return environment_path
    template_path = repository_root / "config/mygpt.env.example"
    content = template_path.read_text(encoding="utf-8")
    content = content.replace("SECRET_KEY=", f"SECRET_KEY={secrets.token_urlsafe(48)}")
    content = content.replace(
        "POSTGRES_PASSWORD=", f"POSTGRES_PASSWORD={secrets.token_urlsafe(32)}"
    )
    environment_path.write_text(content, encoding="utf-8")
    os.chmod(environment_path, 0o600)
    return environment_path


def docker_is_ready() -> bool:
    """Report whether Docker Desktop is installed and its daemon is reachable."""
    if shutil.which("docker") is None:
        return False
    result = subprocess.run(
        ["docker", "info"],
        capture_output=True,
        check=False,
        text=True,
    )
    return result.returncode == 0


def ollama_model_is_ready(model: str) -> bool:
    """Return whether the host Ollama server has the required model installed."""
    if shutil.which("ollama") is None:
        return False
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode != 0:
        return False
    installed_names = {line.split()[0] for line in result.stdout.splitlines() if line.split()}
    return model in installed_names or f"{model}:latest" in installed_names


def pull_ollama_model(model: str) -> None:
    """Download an explicitly requested host Ollama model and verify it is available."""
    if shutil.which("ollama") is None:
        raise RuntimeError("Ollama must be installed before its model can be downloaded")
    subprocess.run(["ollama", "pull", model], check=True)
    if not ollama_model_is_ready(model):
        raise RuntimeError(f"Ollama did not make the required model {model!r} available")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--skills-root", type=Path, default=DEFAULT_SKILLS_ROOT)
    parser.add_argument(
        "--bootstrap-rag",
        action="store_true",
        help="Start containers and import the full pinned Turing Way corpus into MyGPT.",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove only this project's managed OpenCode MCP entry, instruction, and skill links.",
    )
    parser.add_argument(
        "--pull-ollama-model",
        action="store_true",
        help="Explicitly download missing required Ollama chat and embedding models.",
    )
    args = parser.parse_args()
    if args.uninstall and (args.bootstrap_rag or args.pull_ollama_model):
        parser.error("--uninstall cannot be used with bootstrap or model-pull options")

    if args.uninstall:
        config_removed = remove_opencode_config(args.config, ROOT)
        removed_links = remove_skill_links(args.skills_root)
        print(f"Removed managed OpenCode configuration: {config_removed}")
        print(f"Removed managed skill links: {len(removed_links)}")
        print("Docker containers, volumes, and unrelated OpenCode settings were preserved.")
        return 0

    if not docker_is_ready():
        print(
            "Docker Desktop is required and must be running before installation. "
            f"Install or start it: {DOCKER_DESKTOP_URL}",
            file=sys.stderr,
        )
        return 2
    missing_models = [model for model in REQUIRED_OLLAMA_MODELS if not ollama_model_is_ready(model)]
    if missing_models:
        if args.pull_ollama_model:
            try:
                for model in missing_models:
                    pull_ollama_model(model)
            except RuntimeError as error:
                print(str(error), file=sys.stderr)
                return 2
        else:
            print(
                "The host Ollama models "
                f"{', '.join(repr(model) for model in missing_models)} are required. "
                "Install them with `ollama pull <model>`, or rerun with "
                "--pull-ollama-model to explicitly authorize the download.",
                file=sys.stderr,
            )
            return 2
    unavailable_models = [
        model for model in REQUIRED_OLLAMA_MODELS if not ollama_model_is_ready(model)
    ]
    if unavailable_models:
        print(
            f"The host Ollama models {', '.join(repr(model) for model in unavailable_models)} "
            "are unavailable after download.",
            file=sys.stderr,
        )
        return 2

    update_opencode_config(args.config, ROOT)
    install_skill_links(args.skills_root, ROOT)
    environment_path = create_mygpt_environment(ROOT)
    print(f"Configured OpenCode: {args.config}")
    print(f"Linked canonical skills: {args.skills_root}")
    print(f"Created or reused local MyGPT settings: {environment_path}")
    if args.bootstrap_rag:
        subprocess.run(
            ["docker", "compose", "up", "--detach", "--build", "--wait"],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(
            ["docker", "compose", "--profile", "bootstrap", "run", "--rm", "mygpt-bootstrap"],
            cwd=ROOT,
            check=True,
        )
        print("RAG bootstrap complete.")
    else:
        print("Start the services with: docker compose up --detach --build")
        print(
            "Initialize RAG with: "
            "python3 scripts/install_opencode.py --bootstrap-rag --pull-ollama-model"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
