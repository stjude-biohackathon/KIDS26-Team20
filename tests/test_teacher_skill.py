from pathlib import Path

from learning_assistant.skill_validation import parse_skill, validate_skill

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".agents/skills/teacher-skill"
TECHNIQUES_PATH = SKILL_ROOT / "references/teaching-techniques.md"
SKILL_PATH = SKILL_ROOT / "SKILL.md"


def test_teacher_skill_frontmatter_is_valid() -> None:
    frontmatter, body = parse_skill(SKILL_PATH)

    assert frontmatter["name"] == "teacher-skill"
    assert validate_skill(SKILL_PATH) == []
    assert "references/teaching-techniques.md" in body


def test_teacher_skill_workflow_covers_core_techniques() -> None:
    _, body = parse_skill(SKILL_PATH)

    required_phrases = (
        "Find the learner's entry point",
        "before explaining",
        "small, self-contained chunks",
        "narrate your reasoning",
        "diagnostic check",
        "growth-mindset",
        "accessibility",
    )
    for phrase in required_phrases:
        assert phrase in body


def test_teacher_skill_stops_teaching_on_request() -> None:
    _, body = parse_skill(SKILL_PATH)

    assert "stop teaching mode and comply immediately" in body


def test_teacher_skill_confirms_user_is_a_student_before_teaching() -> None:
    _, body = parse_skill(SKILL_PATH)

    required_phrases = (
        "Confirm the user's profile before teaching anything",
        "do not use this skill",
        "give a normal, direct answer instead",
    )
    for phrase in required_phrases:
        assert phrase in body


def test_teaching_techniques_reference_cites_both_grounded_sources() -> None:
    text = TECHNIQUES_PATH.read_text(encoding="utf-8")

    assert "book.the-turing-way.org/pathways/pathways" in text
    assert "carpentries.github.io/lesson-development-training" in text
    assert "carpentries.github.io/instructor-training" in text
    assert "CC BY 4.0" in text


def test_teaching_techniques_reference_includes_throughline_and_citation() -> None:
    text = TECHNIQUES_PATH.read_text(encoding="utf-8")

    assert "Give the chunks a throughline" in text
    assert "carpentries.github.io/lesson-development-training/narrative.html" in text
    assert "Kirschner, P. A., Sweller, J., & Clark, R. E. (2006)" in text
