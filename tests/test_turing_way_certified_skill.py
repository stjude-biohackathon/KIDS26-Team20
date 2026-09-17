import re
from pathlib import Path

from learning_assistant.skill_validation import parse_skill, validate_skill

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / ".agents/skills/turing-way-certified/SKILL.md"

CRITERIA = (
    "Project purpose and scope",
    "Version control and provenance",
    "Open collaboration",
    "Reproducible environments",
    "Data and workflow provenance",
    "Testing and validation",
    "Automation and continuous integration",
    "Documentation and usability",
    "Licensing, attribution, and responsible reuse",
    "Ethics, accessibility, and sustainability",
)


def test_certified_skill_frontmatter_and_tools_are_valid() -> None:
    frontmatter, body = parse_skill(SKILL_PATH)

    assert frontmatter["name"] == "turing-way-certified"
    assert "public GitHub repository" in frontmatter["description"]
    assert "public commit-pinned GitHub evidence URLs" in frontmatter["compatibility"]
    assert frontmatter["metadata"] == {
        "audience": "research-software-teams-and-maintainers",
        "status": "draft",
    }
    assert validate_skill(SKILL_PATH) == []

    required_tools = (
        "learning-assistant_get_turing_way_review_evidence",
        "learning-assistant_list_resources",
        "learning-assistant_get_resource",
        "learning-assistant_get_turing_way_evidence_packets",
        "learning-assistant_render_validated_turing_way_review",
    )
    for tool in required_tools:
        assert f"`{tool}`" in body


def test_certified_skill_has_exactly_ten_scored_criteria_and_100_point_total() -> None:
    _, body = parse_skill(SKILL_PATH)
    rubric = body.split("## Ten-criterion rubric", 1)[1].split("## Workflow", 1)[0]
    rows = re.findall(r"^(\d+)\. \*\*(.+?):\*\*", rubric, re.MULTILINE)

    assert tuple(name for _, name in rows) == CRITERIA
    assert [int(number) for number, _ in rows] == list(range(1, 11))
    assert "Score every criterion from 0 to 10" in rubric
    assert "The total is out\nof 100." in rubric
    assert "`total = sum(score_1 ... score_10)`" in body
    assert "report it as `N/100` and\n  `N%`" in body


def test_certified_skill_requires_public_commit_pinned_repository_evidence() -> None:
    frontmatter, body = parse_skill(SKILL_PATH)

    assert "authorized local checkout" not in frontmatter["compatibility"]
    assert "Do not review a\n   private or local-only repository." in body
    assert (
        "A local checkout may be used for inspection only\n"
        "   when it corresponds to that public repository"
    ) in body
    assert (
        "every cited fact can be\n   proven with a public, commit-pinned GitHub evidence URL"
        in body
    )
    assert (
        "If the repository is private or local-only, explain that the evidence-packet\n"
        "contract requires public, commit-pinned GitHub URLs and do not score it."
    ) in body


def test_certified_skill_defines_pdf_and_auditable_source_contract() -> None:
    _, body = parse_skill(SKILL_PATH)
    normalized_body = " ".join(body.split())

    required_phrases = (
        "TURING_WAY_CERTIFIED_REPORT.pdf",
        "TURING_WAY_CERTIFIED_REPORT.md",
        "or `.html` so the PDF is auditable",
        "contains all ten criteria and the total score",
        "preserves source repository, path, ref, and URL for every citation",
        "do not claim that a PDF was generated",
    )
    for phrase in required_phrases:
        assert phrase in normalized_body


def test_certified_skill_handles_renderer_scope_without_inventing_a_rating() -> None:
    _, body = parse_skill(SKILL_PATH)

    assert "when its contract applies" in body
    assert (
        "If that renderer cannot represent all ten criteria, preserve its validated\n   evidence"
    ) in body
    assert "without\n   fabricating a canonical rating" in body
    assert "Do not\n   manually present a competing Turing Way rating" in body


def test_certified_skill_defines_failure_and_non_certification_boundaries() -> None:
    _, body = parse_skill(SKILL_PATH)

    required_phrases = (
        "not official certification",
        "do not score it",
        "do not invent\ncitations",
        "If public evidence is incomplete",
        "lower confidence",
        "Never silently replace a missing source",
        "scientific validity, security, legal\n  compliance, or institutional endorsement",
    )
    for phrase in required_phrases:
        assert phrase in body
