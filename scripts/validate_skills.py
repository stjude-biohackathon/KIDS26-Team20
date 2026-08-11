"""CLI wrapper for canonical Agent Skill validation."""

from __future__ import annotations

from pathlib import Path

from learning_assistant.skill_validation import validate_skills

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents/skills"


def main() -> int:
    return validate_skills(SKILLS_ROOT, ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
