from pathlib import Path

from learning_assistant.skill_validation import validate_skill

ROOT = Path(__file__).resolve().parents[1]


def test_all_canonical_skills_are_valid() -> None:
    skill_files = sorted((ROOT / ".agents/skills").glob("*/SKILL.md"))
    assert skill_files
    failures = {str(path): validate_skill(path) for path in skill_files if validate_skill(path)}
    assert failures == {}


def test_turing_way_review_skill_uses_the_citation_preserving_mcp_tools() -> None:
    skill = ROOT / ".agents/skills/turing-way-review/SKILL.md"
    text = skill.read_text(encoding="utf-8")

    assert "Review a research software repository" in text
    assert "`learning-assistant_list_resources`" in text
    assert "`learning-assistant_get_resource`" in text
    assert "`learning-assistant_get_turing_way_evidence_packets`" in text
    assert "`learning-assistant_get_turing_way_review_evidence`" in text
    assert "required MyGPT RAG evidence" in text
    assert "MyGPT RAG relevance: N%" in text
    assert "Do not\n   estimate, normalize, omit, or invent" in text
    assert "## Required report format" in text
    assert "exact, direct public GitHub URL\n   that proves that fact" in text
    assert "Each fact entry must describe one fact only" in text
    assert "separate fact entries and a separate proving URL\n   for every part" in text
    assert "related or nearby file is not evidence for an unshown\n   fact" in text
    assert "every content claim uses the exact public GitHub file or\ncommit URL" in text
    assert (
        "every absence claim uses the exact\npublic GitHub repository tree or API listing URL"
        in text
    )
    assert "A\nstandalone bibliography, an uncited improvement" in text
    assert "do\nnot assign a rating" in text
    assert "rating out of 6" in text
    assert "not a certification" in text


def test_agent_guidance_routes_scientist_requests_to_turing_way_skills() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "`turing-way-guidance` skill" in text
    assert "`turing-way-review`" in text
    assert "`turing-way-pathfinder` skill" in text
    assert "learning-assistant MCP" in text
    assert "learning-assistant_get_turing_way_evidence_packets" in text


def test_turing_way_guidance_requires_citation_safe_evidence_packets() -> None:
    skill = ROOT / ".agents/skills/turing-way-guidance/SKILL.md"
    text = skill.read_text(encoding="utf-8")

    assert "`learning-assistant_get_turing_way_evidence_packets`" in text
    assert "MyGPT RAG relevance: N%" in text
    assert "one exact supporting `resource_id` per step" in text


def test_readme_explains_the_evidence_packet_provenance_boundary() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "`get_turing_way_evidence_packets`" in text
    assert "repository URL supports the factual claim" in text
    assert "retrieval-match score" in text


def test_turing_way_pathfinder_uses_curated_paths_and_targeted_rag() -> None:
    skill = ROOT / ".agents/skills/turing-way-pathfinder/SKILL.md"
    text = skill.read_text(encoding="utf-8")

    assert "`learning-assistant_get_turing_way_evidence_packets`" in text
    assert "Early Career Researchers" in text
    assert "Project Leaders" in text
    assert "Research Software Engineers" in text
    assert "Data Stewards" in text
    assert "MyGPT RAG relevance: N%" in text
    assert "Ask only for missing intake information." in text
    assert "MUST NOT** ask, confirm, or request any\n   additional intake" in text
    assert "Proceed directly to pathway selection" in text
    assert "resource and evidence-packet retrieval" in text
    assert "Starting, analysis underway, or" in text
    assert "pathways/pathways-early-career-researchers" in text
    assert "reuse one URL for unrelated chapters" in text
    assert "private life, identity" in text
    assert "Always call `learning-assistant_list_resources` before" in text
    assert "Do not retrieve a known ID directly." in text
    assert "its own observable completion checkpoint" in text
    assert "Finish the response immediately after the last action's completion checkpoint." in text
    assert "Do not add a shared final checkpoint" in text
