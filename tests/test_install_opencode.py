import json
from pathlib import Path

import pytest

from scripts import install_opencode
from scripts.install_opencode import (
    CANONICAL_SKILLS,
    create_mygpt_environment,
    install_skill_links,
    pull_ollama_model,
    remove_opencode_config,
    remove_skill_links,
    update_opencode_config,
)

ROOT = Path(__file__).resolve().parents[1]


def test_installer_preserves_existing_config_and_registers_mcp(tmp_path: Path) -> None:
    config_path = tmp_path / "opencode.json"
    agent_instructions = str(ROOT / "AGENTS.md")
    config_path.write_text(
        json.dumps(
            {
                "model": "test/model",
                "instructions": [agent_instructions, "shared.md", agent_instructions],
            }
        ),
        encoding="utf-8",
    )

    update_opencode_config(config_path, ROOT)
    first_install = config_path.read_text(encoding="utf-8")
    update_opencode_config(config_path, ROOT)

    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert config["model"] == "test/model"
    assert config["mcp"]["turing-way-mygpt"]["url"] == "http://127.0.0.1:8000/mcp"
    assert config["instructions"] == [agent_instructions, "shared.md"]
    assert config["permission"]["skill"]["turing-way-*"] == "allow"
    assert config_path.read_text(encoding="utf-8") == first_install


def test_installer_links_global_skills_to_canonical_repository_files(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"

    install_skill_links(skills_root, ROOT)

    for name in CANONICAL_SKILLS:
        target = skills_root / name
        assert target.is_symlink()
        assert target.resolve() == ROOT / ".agents/skills" / name


def test_installer_replaces_a_stale_managed_skill_symlink(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    skills_root.mkdir()
    stale_target = tmp_path / "stale-skill"
    stale_target.mkdir()
    (skills_root / "turing-way-review").symlink_to(stale_target, target_is_directory=True)

    install_skill_links(skills_root, ROOT)

    assert (skills_root / "turing-way-review").resolve() == (
        ROOT / ".agents/skills" / "turing-way-review"
    )


def test_uninstaller_removes_only_managed_opencode_entries(tmp_path: Path) -> None:
    config_path = tmp_path / "opencode.json"
    config_path.write_text(
        json.dumps(
            {
                "instructions": ["shared.md", str(ROOT / "AGENTS.md")],
                "mcp": {"other-server": {"type": "local"}, "turing-way-mygpt": {"type": "remote"}},
            }
        ),
        encoding="utf-8",
    )
    skills_root = tmp_path / "skills"
    install_skill_links(skills_root, ROOT)
    (skills_root / "unrelated").mkdir()

    assert remove_opencode_config(config_path, ROOT) is True
    assert remove_opencode_config(config_path, ROOT) is False
    assert remove_skill_links(skills_root)
    assert remove_skill_links(skills_root) == []

    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert config["instructions"] == ["shared.md"]
    assert config["mcp"] == {"other-server": {"type": "local"}}
    assert (skills_root / "unrelated").is_dir()
    assert all(not (skills_root / name).exists() for name in CANONICAL_SKILLS)


def test_installer_does_not_replace_a_non_symlink_skill_directory(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    (skills_root / "turing-way-review").mkdir(parents=True)

    with pytest.raises(FileExistsError, match="refusing to replace"):
        install_skill_links(skills_root, ROOT)


def test_installer_creates_private_mygpt_settings_only_once(tmp_path: Path) -> None:
    config_directory = tmp_path / "config"
    config_directory.mkdir()
    (config_directory / "mygpt.env.example").write_text(
        "SECRET_KEY=\nPOSTGRES_DB=mygpt\nPOSTGRES_USER=mygpt\nPOSTGRES_PASSWORD=\n",
        encoding="utf-8",
    )

    created = create_mygpt_environment(tmp_path)
    original_content = created.read_text(encoding="utf-8")
    reused = create_mygpt_environment(tmp_path)

    assert reused == created
    assert created.read_text(encoding="utf-8") == original_content
    assert "SECRET_KEY=\n" not in original_content
    assert "POSTGRES_PASSWORD=\n" not in original_content


def test_installer_detects_missing_or_unreachable_docker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(install_opencode.shutil, "which", lambda _command: None)
    assert install_opencode.docker_is_ready() is False

    monkeypatch.setattr(install_opencode.shutil, "which", lambda _command: "docker")
    monkeypatch.setattr(
        install_opencode.subprocess,
        "run",
        lambda *_args, **_kwargs: type("Result", (), {"returncode": 1})(),
    )
    assert install_opencode.docker_is_ready() is False


def test_installer_detects_required_host_ollama_model(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(install_opencode.shutil, "which", lambda _command: "ollama")
    monkeypatch.setattr(
        install_opencode.subprocess,
        "run",
        lambda *_args, **_kwargs: type(
            "Result",
            (),
            {"returncode": 0, "stdout": "NAME ID SIZE MODIFIED\nqwen2.5:3b abc 1.9GB today\n"},
        )(),
    )

    assert install_opencode.ollama_model_is_ready("qwen2.5:3b") is True
    assert install_opencode.ollama_model_is_ready("gemma3:27b") is False


def test_installer_pulls_an_explicitly_requested_ollama_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commands: list[list[str]] = []
    monkeypatch.setattr(install_opencode.shutil, "which", lambda _command: "ollama")
    monkeypatch.setattr(
        install_opencode.subprocess,
        "run",
        lambda command, **_kwargs: (
            commands.append(command)
            or type(
                "Result",
                (),
                {"returncode": 0, "stdout": "qwen2.5:3b abc 1.9GB today\n"},
            )()
        ),
    )

    pull_ollama_model("qwen2.5:3b")

    assert commands == [["ollama", "pull", "qwen2.5:3b"], ["ollama", "list"]]
