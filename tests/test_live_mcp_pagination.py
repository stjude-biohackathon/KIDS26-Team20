"""Opt-in checks against a deployed MCP server and its approved Turing Way corpus."""

import asyncio
import json
import math
import os
import re

import pytest
from mcp import Client

from learning_assistant.models import (
    ResourceDocument,
    ResourceSummary,
    TuringWayEvidencePacket,
)

LIVE_MCP_URL = os.environ.get("LEARNING_ASSISTANT_LIVE_MCP_URL")
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not LIVE_MCP_URL,
        reason="Set LEARNING_ASSISTANT_LIVE_MCP_URL to opt in to live MCP and MyGPT calls.",
    ),
]

CHAPTER_PATHS = {
    "vcs": "book/website/reproducible-research/vcs.md",
    "reviewing": "book/website/reproducible-research/reviewing.md",
    "renv": "book/website/reproducible-research/renv.md",
    "testing": "book/website/reproducible-research/testing.md",
    "ci": "book/website/reproducible-research/ci.md",
    "code-quality": "book/website/reproducible-research/code-quality.md",
    "code-documentation": "book/website/reproducible-research/code-documentation.md",
    "code-reuse": "book/website/reproducible-research/code-reuse.md",
    "licensing": "book/website/reproducible-research/licensing.md",
    "open": "book/website/reproducible-research/open.md",
    "pd-overview": "book/website/project-design/pd-overview.md",
    "persona": "book/website/project-design/stakeholders/persona.md",
    "coc": "book/website/community-handbook/coc.md",
    "contributing": "book/website/community-handbook/contributing.md",
    "collaboration": "book/website/collaboration/collaboration.md",
}
CLAIMS = {
    "vcs": "Track changes to research software using version control.",
    "renv": "Record software dependencies and versions to make environments reproducible.",
    "testing": "Use repeatable automated tests to detect software regressions.",
    "ci": "Run automated checks in continuous integration when code changes.",
    "code-quality": "Use consistent coding style and static analysis for code quality.",
    "code-documentation": "Document setup and usage so others can understand research software.",
    "licensing": "Specify a license to clarify how others may reuse research software.",
    "persona": "Identify stakeholders and their participation pathways in a research project.",
}


async def test_live_paginated_discovery_and_evidence_for_all_healthcheck_categories() -> None:
    assert LIVE_MCP_URL is not None
    async with Client(LIVE_MCP_URL) as client:
        tools = await client.list_tools()
        listing_tool = next(tool for tool in tools.tools if tool.name == "list_resources")
        assert listing_tool.input_schema["properties"]["offset"]["default"] == 0
        assert listing_tool.input_schema["properties"]["offset"]["minimum"] == 0

        resources: list[ResourceSummary] = []
        page_sizes: list[int] = []
        for _ in range(50):
            result = await client.call_tool(
                "list_resources", {"limit": 200, "offset": len(resources)}
            )
            assert not result.is_error and result.structured_content is not None
            page = [
                ResourceSummary.model_validate(entry)
                for entry in result.structured_content["result"]
            ]
            assert len(page) <= 200
            resources.extend(page)
            page_sizes.append(len(page))
            ids = [entry.resource_id for entry in resources]
            assert ids == sorted(set(ids)), "Pages must be stable, sorted, and non-overlapping."
            if len(page) < 200:
                break
        else:
            pytest.fail("Discovery did not terminate within 50 pages.")

        assert len(resources) > 200, "Live test must exercise discovery beyond the old cap."
        by_path = {entry.path: entry for entry in resources}
        missing = set(CHAPTER_PATHS.values()) - by_path.keys()
        assert not missing, f"Required healthcheck chapters were not discovered: {sorted(missing)}"
        at_end = await client.call_tool("list_resources", {"limit": 200, "offset": len(resources)})
        assert not at_end.is_error and at_end.structured_content == {"result": []}
        default = await client.call_tool("list_resources", {})
        assert default.structured_content == {
            "result": [entry.model_dump() for entry in resources[:25]]
        }
        invalid = await client.call_tool("list_resources", {"offset": -1})
        assert invalid.is_error

        results = await asyncio.gather(
            *(
                client.call_tool("get_resource", {"resource_id": by_path[path].resource_id})
                for path in CHAPTER_PATHS.values()
            )
        )
        documents: dict[str, ResourceDocument] = {}
        for key, result in zip(CHAPTER_PATHS, results, strict=True):
            assert not result.is_error and result.structured_content is not None
            document = ResourceDocument.model_validate(result.structured_content)
            listed = by_path[CHAPTER_PATHS[key]]
            assert document.content.strip()
            assert document.resource_id == listed.resource_id
            assert document.path == listed.path and document.url == listed.url
            assert document.origin == "github"
            assert document.repository == "the-turing-way/the-turing-way"
            assert re.fullmatch(r"[0-9a-f]{40}", document.ref)
            assert document.url == (
                f"https://github.com/{document.repository}/blob/{document.ref}/{document.path}"
            )
            documents[key] = document

        status = await client.call_tool("get_rag_status", {})
        assert not status.is_error and status.structured_content is not None
        assert status.structured_content["status"] == "ready"
        assert status.structured_content["source_count"] > 0
        aggregate = await client.call_tool("get_turing_way_review_evidence", {})
        assert not aggregate.is_error and aggregate.structured_content is not None
        areas = aggregate.structured_content["result"]
        assert {area["area"] for area in areas} == {
            "project design",
            "reproducibility",
            "version control and collaboration",
        }
        assert all(area["retrieval"]["context"] and area["retrieval"]["sources"] for area in areas)

        keys = list(CLAIMS)
        scores: dict[str, float] = {}
        for start in range(0, len(keys), 5):
            batch = keys[start : start + 5]
            result = await client.call_tool(
                "get_turing_way_evidence_packets",
                {
                    "requests": [
                        {"claim": CLAIMS[key], "resource_id": documents[key].resource_id}
                        for key in batch
                    ]
                },
            )
            assert not result.is_error and result.structured_content is not None
            packets = [
                TuringWayEvidencePacket.model_validate(packet)
                for packet in result.structured_content["result"]
            ]
            for key, packet in zip(batch, packets, strict=True):
                document = documents[key]
                assert packet.claim == CLAIMS[key]
                assert packet.repository_fact is None
                assert packet.citation.model_dump() == document.model_dump(exclude={"content"})
                assert packet.retrieval.context.strip() and packet.retrieval.sources
                assert packet.retrieval.relevance_score is not None
                assert math.isfinite(packet.retrieval.relevance_score)
                scores[key] = packet.retrieval.relevance_score

        print(
            json.dumps(
                {
                    "resources": len(resources),
                    "page_sizes": page_sizes,
                    "chapters_read": len(documents),
                    "evidence_packets": len(scores),
                    "relevance_scores": scores,
                }
            )
        )
