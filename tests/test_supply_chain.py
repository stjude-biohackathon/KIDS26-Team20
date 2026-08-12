"""Regression tests: every external input is pinned; installs never run scripts."""

import json
import re
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

OPERATIONAL_FILES = (
    "config/workbench-env.sh",
    "scripts/project.py",
    "scripts/workbench.py",
)


def test_node_tools_are_locked_with_integrity() -> None:
    manifest = json.loads((ROOT / "tools/package.json").read_text(encoding="utf-8"))
    assert manifest["dependencies"] == {
        "@modelcontextprotocol/inspector": "2.0.0",
        "opencode-ai": "1.18.9",
    }
    lock = json.loads((ROOT / "tools/package-lock.json").read_text(encoding="utf-8"))
    assert lock["lockfileVersion"] >= 3
    for name, meta in lock["packages"].items():
        if name == "" or meta.get("link") or meta.get("inBundle"):
            continue
        assert re.match(r"^sha(512|256)-", meta.get("integrity", "")), name
        assert meta.get("resolved", "").startswith("https://registry.npmjs.org/"), name


def test_tools_task_installs_from_lockfile_without_scripts() -> None:
    text = (ROOT / "scripts/project.py").read_text(encoding="utf-8")
    assert '"ci", "--ignore-scripts"' in text
    assert "--global" not in text
    # opencode-ai stages its platform binary in its own postinstall; scripts
    # run for that single integrity-verified package only.
    assert '"rebuild", "opencode-ai", "--ignore-scripts=false"' in text


def test_no_floating_package_execution_in_operational_files() -> None:
    # Matches the bare command token, so splitting it across argument literals
    # (`run("npx", "--yes", ...)`) cannot slip past this check.
    npx_command = re.compile(r"(?<![\w-])npx(?![\w-])")
    for relative in OPERATIONAL_FILES:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert not npx_command.search(text), relative
        assert "@latest" not in text, relative


def test_provider_sdk_reference_is_exactly_versioned() -> None:
    from scripts.workbench import PROVIDER_SDK_PACKAGE

    assert re.fullmatch(r"@ai-sdk/openai-compatible@\d+\.\d+\.\d+", PROVIDER_SDK_PACKAGE)


def test_build_backend_is_exactly_pinned() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    for requirement in pyproject["build-system"]["requires"]:
        assert re.fullmatch(r"[A-Za-z0-9._-]+==[0-9][A-Za-z0-9.]*", requirement), requirement


def test_python_lock_is_fully_hash_pinned_to_pypi() -> None:
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    for package in lock["package"]:
        source = package.get("source", {})
        if source.get("editable"):
            continue
        assert source.get("registry") == "https://pypi.org/simple", package["name"]
        artifacts = list(package.get("wheels", []))
        if "sdist" in package:
            artifacts.append(package["sdist"])
        assert artifacts, package["name"]
        for artifact in artifacts:
            assert artifact["hash"].startswith("sha256:"), package["name"]


def test_enabled_corpus_sources_use_commit_pins() -> None:
    for manifest in (ROOT / "corpus/sources.yaml", ROOT / "corpus/sources.live.yaml"):
        data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        for source in data["sources"]:
            # Both keys default the same way the SourceConfig model does, so a
            # source that omits them is still checked instead of skipped.
            if source.get("enabled", True):
                assert re.fullmatch(r"[0-9a-f]{40}", source.get("ref", "main")), (
                    f"{manifest.name}: {source['id']}"
                )
