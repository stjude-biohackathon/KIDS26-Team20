from pathlib import Path

from learning_assistant.skill_validation import validate_skill

ROOT = Path(__file__).resolve().parents[1]


def test_all_canonical_skills_are_valid() -> None:
    skill_files = sorted((ROOT / ".agents/skills").glob("*/SKILL.md"))
    assert skill_files
    failures = {str(path): validate_skill(path) for path in skill_files if validate_skill(path)}
    assert failures == {}
