import json
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENV_KEYS = {
    "AIMAAS_BASE_URL",
    "AIMAAS_MODEL_ID",
    "AIMAAS_API_KEY",
    "AIMAAS_API_KEY_HEADER",
}


def _parse_env_template(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key, value = stripped.split("=", 1)
        values[key] = value
    return values


def test_workbench_env_template_is_sanitized() -> None:
    values = _parse_env_template(ROOT / "config/workbench.env.example")
    assert set(values) == ENV_KEYS
    assert values["AIMAAS_BASE_URL"] == ""
    assert values["AIMAAS_MODEL_ID"] == ""
    assert values["AIMAAS_API_KEY"] == ""
    assert values["AIMAAS_API_KEY_HEADER"] == "api-key"


def test_local_workbench_inputs_are_ignored() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

    # The template's .env rules match only a file named exactly .env, so this
    # entry is the one thing keeping the personal API key out of the repository.
    assert "config/workbench.env" in gitignore
    assert "tools/node_modules/" in gitignore


def test_workbench_env_loader_allowlists_keys_and_never_executes_the_file() -> None:
    text = (ROOT / "config/workbench-env.sh").read_text(encoding="utf-8")
    for key in sorted(ENV_KEYS):
        assert key in text
    assert "export" in text
    assert "while IFS= read" in text
    assert "source" not in text


def test_opencode_uses_pinned_superpowers_and_safe_defaults() -> None:
    config = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
    assert config["autoupdate"] is False
    assert config["share"] == "disabled"
    assert config["plugin"] == [
        "superpowers@git+https://github.com/obra/superpowers.git#"
        "d884ae04edebef577e82ff7c4e143debd0bbec99"
    ]
    assert config["mcp"]["learning-assistant"]["type"] == "local"


def test_project_runner_exposes_workbench_commands() -> None:
    text = (ROOT / "scripts/project.py").read_text(encoding="utf-8")
    assert 'task == "tools"' in text
    assert 'task == "doctor"' in text
    assert 'task == "workbench-config"' in text
    assert 'task == "model-preflight"' in text
    assert 'task == "workbench-check"' in text


def test_opencode_launches_the_mcp_server_and_skills_without_extra_setup() -> None:
    config = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
    server = config["mcp"]["learning-assistant"]
    assert server["enabled"] is True
    assert server["command"] == ["uv", "run", "learning-assistant", "stdio"]
    # OpenCode discovers .agents/skills at the project level on its own, so the
    # offline corpus must be committed for those tools to return citations.
    assert (ROOT / ".agents/skills/skill-template/SKILL.md").exists()
    assert list((ROOT / "corpus/fixtures/turing-way").glob("*.md"))


def test_no_tracked_file_contains_a_live_provider_value() -> None:
    """The repository is published, so a real gateway value must never be tracked.

    Skipped when a contributor has not filled in their local settings, which is
    the normal state in CI.
    """
    env_file = ROOT / "config/workbench.env"
    if not env_file.exists():
        pytest.skip("no local provider settings on this machine")

    values = dict(
        line.split("=", 1)
        for line in env_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#") and "=" in line
    )
    needles = {
        name: value.strip()
        for name, value in values.items()
        # The header name is a published HTTP convention, not a secret.
        if value.strip() and name != "AIMAAS_API_KEY_HEADER"
    }
    base_url = values.get("AIMAAS_BASE_URL", "").strip()
    if base_url:
        parsed = urlsplit(base_url)
        if parsed.hostname:
            needles["gateway host"] = parsed.hostname
        deployment = parsed.path.strip("/").split("/")[0]
        if deployment:
            needles["deployment name"] = deployment

    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()

    leaks = []
    for relative in tracked:
        path = ROOT / relative
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # Report only the field name; never put the value in the failure output.
        leaks += [f"{relative}: {label}" for label, needle in needles.items() if needle in content]

    assert not leaks, f"tracked files contain live provider values: {sorted(leaks)}"


def test_skills_directory_documents_where_participants_add_skills() -> None:
    readme = ROOT / ".agents/skills/README.md"
    assert readme.exists(), "participants need an explainer at the root of the skills directory"
    text = readme.read_text(encoding="utf-8")
    assert ".agents/skills/<your-skill-name>/SKILL.md" in text
    assert "scripts/validate_skills.py" in text
    # A loose README must not be mistaken for a skill by the validator.
    assert not (ROOT / ".agents/skills/README.md").is_dir()


def test_doctor_reports_every_launch_dependency() -> None:
    text = (ROOT / "scripts/doctor.py").read_text(encoding="utf-8")
    for label in (
        "Python environment",
        "Turing Way MCP server",
        "OpenCode launch configuration",
        "Project skills",
        "Node.js",
        "OpenCode install",
        "Model provider",
    ):
        assert label in text


def test_doctor_never_echoes_a_credential_value(monkeypatch: pytest.MonkeyPatch) -> None:
    from scripts.doctor import check_provider

    secret = "super-secret-key-value"
    monkeypatch.setenv("AIMAAS_BASE_URL", "https://provider.example/deployment/openai/v1")
    monkeypatch.setenv("AIMAAS_MODEL_ID", "approved-model")
    monkeypatch.setenv("AIMAAS_API_KEY", secret)

    result = check_provider()

    assert secret not in result.summary + result.action
    assert "provider.example" not in result.summary + result.action


def test_doctor_flags_a_partially_configured_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AIMAAS_BASE_URL", "https://provider.example/deployment/openai/v1")
    monkeypatch.delenv("AIMAAS_MODEL_ID", raising=False)
    monkeypatch.delenv("AIMAAS_API_KEY", raising=False)

    from scripts.doctor import check_provider

    result = check_provider()

    assert result.status == "FAIL"
    assert "AIMAAS_MODEL_ID" in result.summary


def test_vscode_exposes_workbench_tasks() -> None:
    config = json.loads((ROOT / ".vscode/tasks.json").read_text(encoding="utf-8"))
    labels = {task["label"] for task in config["tasks"]}
    assert "Workbench: Model Preflight" in labels
    assert "Workbench: Check" in labels
