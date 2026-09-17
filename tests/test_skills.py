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
    assert "`learning-assistant_render_validated_turing_way_review`" in text
    assert "`learning-assistant_validate_turing_way_review`" in text
    assert "required MyGPT RAG evidence" in text
    assert "Do not estimate, normalize, omit, or invent a relevance score." in text
    assert "exact, direct public GitHub URL\n   that proves that fact" in text
    assert "Each recommendation and fact entry must describe one fact only" in text
    assert "separate fact entries and a separate proving URL\n   for every part" in text
    assert "related or nearby file is not evidence for an unshown\n   fact" in text
    assert (
        "A positive file URL proves only the content it displays and must not\n"
        "   be used to prove the absence of unrelated files"
    ) in text
    assert (
        "Each separately asserted\n"
        "   absence requires its own repository-fact entry and exact tree or API-listing\n"
        "   URL" in text
    )
    assert (
        "one exact GitHub recursive-tree or API listing demonstrably\n"
        "   covers every claimed path at the checked commit" in text
    )
    assert "Use the exact commit SHA,\n   never a mutable branch or tag" in text
    assert 'confirm that its response has `"truncated": false`' in text
    assert "A single commit page proves only that commit's\n   content" in text
    assert "/commits/COMMIT" in text
    assert "Do not infer the absence of\n   branches or tags from either URL" in text
    assert "Each row must contain\n   exactly one directly observed claim" in text
    assert "its exact repository evidence URL" in text
    assert (
        "Withhold all area scores and the total if any rationale lacks its required\n"
        "   repository evidence" in text
    )
    assert "single-focus recommendations" in text
    assert "Pass exactly one `repository_fact` in each request" in text
    assert "Do not combine unrelated changes" in text
    assert "This tool subsumes\n   `learning-assistant_validate_turing_way_review`" in text
    assert (
        "The final\n   response must contain exactly its returned `report` field, verbatim." in text
    )
    assert (
        "Do not\n   render `score_section` or `recommendation_evidence_block` separately." in text
    )
    final_response_prohibitions = (
        "agent-written introduction, repository narrative, RAG table,\n"
        "   summary, conclusion, notice, or trailing text"
    )
    assert final_response_prohibitions in text
    assert "## Final response" in text
    assert "The renderer's `report` is the complete and only final response." in text
    assert "Never manually calculate,\n   rewrite, or reformat a score" in text
    assert "Do not invent expected benefits or explanatory prose" in text
    assert "not a certification" in text


def test_agent_guidance_routes_scientist_requests_to_turing_way_skills() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "Use\n`turing-way-guidance` for focused guidance" in text
    assert "`turing-way-review`" in text
    assert "invoke\n`turing-way-pathfinder` first" in text
    assert "Do not combine PathFinder with\n`teacher-skill` or `turing-way-guidance`" in text
    assert "`turing-way-certified`" in text

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


def test_turing_way_certified_requires_full_score_and_pdf_artifacts() -> None:
    skill = ROOT / ".agents/skills/turing-way-certified/SKILL.md"
    text = skill.read_text(encoding="utf-8")

    assert "100-point readiness review" in text
    assert "complete eight-category rubric" in text
    assert "integer score out of 100" in text
    assert "TURING_WAY_CERTIFICATION.md" in text
    assert "TURING_WAY_CERTIFICATION.pdf" in text
    assert "Verify that the file exists and is non-empty" in text
    assert "do not claim that a PDF was generated" in text
    assert "do not substitute the three-area, six-point" in text
