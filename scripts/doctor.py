"""Check that a fresh clone can run OpenCode with the skills and the MCP server.

Every check reports PASS, WARN, or FAIL with the next action to take. WARN means
the offline workbench is fine but the agent interface is not fully wired yet.
No credential value is ever printed.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import shutil
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents/skills"
TOOLS_BIN = ROOT / "tools/node_modules/.bin"
PROVIDER_VALUES = ("AIMAAS_BASE_URL", "AIMAAS_MODEL_ID", "AIMAAS_API_KEY")


@dataclass(frozen=True)
class Result:
    status: str
    summary: str
    action: str = ""


def _ok(summary: str) -> Result:
    return Result("PASS", summary)


def _warn(summary: str, action: str) -> Result:
    return Result("WARN", summary, action)


def _fail(summary: str, action: str) -> Result:
    return Result("FAIL", summary, action)


def _which(command: str) -> str | None:
    search_path = os.pathsep.join([str(TOOLS_BIN), os.environ.get("PATH", "")])
    return shutil.which(command, path=search_path)


def check_python_environment() -> Result:
    try:
        import learning_assistant  # noqa: F401
    except ImportError:
        return _fail(
            "the learning-assistant package is not importable",
            "run: uv sync --extra dev --frozen",
        )
    return _ok(f"Python {sys.version_info.major}.{sys.version_info.minor} environment is ready")


async def _query_mcp(*, offline: bool) -> tuple[set[str], list[dict]]:
    """Start the server in-process and exercise both tools."""
    from mcp import Client

    from learning_assistant.server import create_server
    from learning_assistant.sources import SourceRegistry

    registry = SourceRegistry(ROOT / "corpus/sources.yaml", offline=offline)
    try:
        server = create_server(registry)
        async with Client(server) as client:
            tools_result = await client.list_tools()
            names = {tool.name for tool in tools_result.tools}
            listed = await client.call_tool("list_resources", {"limit": 5})
            entries = (listed.structured_content or {}).get("result", [])
            if entries:
                await client.call_tool(
                    "get_resource",
                    {"resource_id": entries[0]["resource_id"]},
                )
            return names, entries
    finally:
        await registry.close()


def check_mcp_serves_content() -> Result:
    """Prove the server is installed, using the committed snapshot only."""
    try:
        names, entries = asyncio.run(_query_mcp(offline=True))
    except Exception as error:  # noqa: BLE001 - report any startup failure to the contributor
        return _fail(
            f"the MCP server did not start ({type(error).__name__})",
            "run: uv sync --extra dev --frozen, then rerun this check",
        )
    if names != {"list_resources", "get_resource"}:
        return _fail(
            f"the MCP server exposes unexpected tools: {sorted(names)}",
            "report this; the server contract is broken",
        )
    if not entries:
        return _fail(
            "the MCP server returned no resources",
            "confirm corpus/fixtures/turing-way is present in this clone",
        )
    return _ok(f"both tools answered; {len(entries)} resource(s) read from the local snapshot")


def check_github_reachable() -> Result:
    """Prove the server can reach GitHub, which is how it works by default."""
    try:
        _, entries = asyncio.run(_query_mcp(offline=False))
    except Exception as error:  # noqa: BLE001 - a network failure must not block offline work
        return _warn(
            f"could not reach GitHub ({type(error).__name__})",
            "check network access; the server falls back to the local snapshot",
        )
    if not entries:
        return _warn(
            "GitHub returned no resources",
            "check the source manifest in corpus/sources.yaml",
        )
    if entries[0].get("origin") != "github":
        return _warn(
            "the server fell back to the local snapshot instead of GitHub",
            "check network access or a GitHub API rate limit; set GITHUB_TOKEN to raise it",
        )
    return _ok("listed resources live from GitHub")


def check_opencode_config() -> Result:
    config_path = ROOT / "opencode.json"
    if not config_path.exists():
        return _fail("opencode.json is missing", "restore it from version control")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    server = config.get("mcp", {}).get("learning-assistant")
    if not server or server.get("enabled") is not True:
        return _fail(
            "opencode.json does not enable the learning-assistant MCP server",
            "restore the mcp.learning-assistant block",
        )
    if not any("superpowers" in entry for entry in config.get("plugin", [])):
        return _warn(
            "opencode.json does not list the Superpowers plugin",
            "add the pinned superpowers entry to the plugin array",
        )
    return _ok("opencode.json starts the MCP server and loads Superpowers on launch")


def check_project_skills() -> Result:
    from learning_assistant.skill_validation import validate_skill

    skill_files = sorted(SKILLS_ROOT.glob("*/SKILL.md"))
    if not skill_files:
        return _fail(
            "no skills found in .agents/skills",
            "confirm this is a complete clone",
        )
    broken = [path.parent.name for path in skill_files if validate_skill(path)]
    if broken:
        return _fail(
            f"invalid skills: {', '.join(broken)}",
            "run: uv run python scripts/validate_skills.py",
        )
    return _ok(f"{len(skill_files)} project skills in .agents/skills are valid and discoverable")


def check_node() -> Result:
    if _which("node") is None:
        return _warn(
            "Node.js was not found, so OpenCode cannot be installed",
            "install Node.js 20 or newer, then open a new terminal",
        )
    return _ok("Node.js is available for OpenCode")


def check_opencode_installed() -> Result:
    if _which("opencode") is None:
        return _warn(
            "OpenCode is not installed in this clone",
            "run: uv run python scripts/project.py tools",
        )
    return _ok("OpenCode is installed from the pinned lockfile")


def check_provider() -> Result:
    configured = [name for name in PROVIDER_VALUES if os.environ.get(name, "").strip()]
    if not configured:
        return _warn(
            "no model provider is loaded in this shell, so OpenCode will start offline",
            "optional: fill config/workbench.env and load it, then run model-preflight",
        )
    if len(configured) < len(PROVIDER_VALUES):
        missing = sorted(set(PROVIDER_VALUES) - set(configured))
        return _fail(
            f"the provider settings are incomplete: {', '.join(missing)} not set",
            "complete config/workbench.env and reload it into this shell",
        )
    return _ok("provider settings are loaded in this shell")


CHECKS: tuple[tuple[str, Callable[[], Result]], ...] = (
    ("Python environment", check_python_environment),
    ("Turing Way MCP server", check_mcp_serves_content),
    ("GitHub connectivity", check_github_reachable),
    ("OpenCode launch configuration", check_opencode_config),
    ("Project skills", check_project_skills),
    ("Node.js", check_node),
    ("OpenCode install", check_opencode_installed),
    ("Model provider", check_provider),
)


def main() -> int:
    # The HTTP client logs every request at INFO, which would bury the report.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    results = [(label, check()) for label, check in CHECKS]
    width = max(len(label) for label, _ in results)
    for label, result in results:
        print(f"{result.status:<4} {label:<{width}}  {result.summary}")
        if result.action:
            print(f"{'':<4} {'':<{width}}  -> {result.action}")

    failures = sum(1 for _, result in results if result.status == "FAIL")
    warnings = sum(1 for _, result in results if result.status == "WARN")
    print()
    if failures:
        print(f"{failures} blocking problem(s). Fix the FAIL lines above and run this again.")
        return 1
    if warnings:
        print(f"Offline workbench is ready. {warnings} optional step(s) remain; see WARN above.")
        return 0
    print("Ready. Start OpenCode from this directory to get the skills and the MCP server.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
