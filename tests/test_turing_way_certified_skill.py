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
    assert "attached local repository" in frontmatter["description"]
    assert "authorized attached local checkout" in frontmatter["compatibility"]
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


def test_certified_skill_supports_public_commit_pinned_repository_evidence() -> None:
    _, body = parse_skill(SKILL_PATH)
    normalized_body = " ".join(body.split())

    assert "For public GitHub input, cite an exact commit-pinned GitHub URL." in normalized_body
    assert (
        "For public absence claims, use a commit-pinned tree or API listing and confirm "
        "recursive API listings are not truncated."
    ) in normalized_body


def test_certified_skill_has_local_evidence_fallback() -> None:
    _, body = parse_skill(SKILL_PATH)
    normalized_body = " ".join(body.split())

    required_phrases = (
        "attached local input, cite only a repository-relative path and line range",
        "never put an absolute local path or private remote URL in the report",
        "`RepositoryFact` contract rejects local paths and private URLs",
        'Label recommendations "locally evidenced; not evidence-packet validated."',
        "In attached local mode, do not call the renderer because it requires public "
        "`RepositoryFact` URLs",
        "switch to the documented local-evidence mode",
        "do not pass local paths or private URLs to the evidence-packet or renderer tools",
    )
    for phrase in required_phrases:
        assert phrase in normalized_body


def test_certified_skill_defines_pdf_and_auditable_source_contract() -> None:
    _, body = parse_skill(SKILL_PATH)
    normalized_body = " ".join(body.split())

    required_phrases = (
        "TURING_WAY_CERTIFIED_REPORT.pdf",
        "TURING_WAY_CERTIFIED_REPORT.md",
        "or `.html` so the PDF is auditable",
        "contains all ten criteria and the total score",
        "For local mode, preserve repository-relative path, line range",
        "do not claim that a PDF was generated",
    )
    for phrase in required_phrases:
        assert phrase in normalized_body


def test_certified_skill_handles_renderer_scope_without_inventing_a_rating() -> None:
    _, body = parse_skill(SKILL_PATH)
    normalized_body = " ".join(body.split())

    assert "when its contract applies" in normalized_body
    assert (
        "If that renderer cannot represent all ten criteria, preserve its validated evidence"
        in normalized_body
    )
    assert "without fabricating a canonical rating" in normalized_body
    assert "Do not manually present a competing Turing Way rating" in normalized_body


def test_certified_skill_defines_failure_and_non_certification_boundaries() -> None:
    _, body = parse_skill(SKILL_PATH)
    normalized_body = " ".join(body.split())

    required_phrases = (
        "not official certification",
        "do not score it",
        "do not invent citations",
        "If evidence is incomplete",
        "lower confidence",
        "Never silently replace a missing source",
        "scientific validity, security, legal compliance, or institutional endorsement",
    )
    for phrase in required_phrases:
        assert phrase in normalized_body
