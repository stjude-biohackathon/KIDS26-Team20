import json
from collections.abc import AsyncIterator
from pathlib import Path

import httpx
import pytest
from mcp import Client
from mcp.types import TextContent

from learning_assistant.models import (
    RepositoryFact,
    ResourceRecord,
    TuringWayReviewScoreRow,
)
from learning_assistant.mygpt import MyGPTClient, MyGPTSettings
from learning_assistant.server import create_server
from learning_assistant.sources import SourceRegistry

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
async def paginated_registry(tmp_path: Path) -> AsyncIterator[SourceRegistry]:
    snapshot = tmp_path / "snapshot"
    filler = snapshot / "a-filler"
    filler.mkdir(parents=True)
    for index in reversed(range(404)):
        (filler / f"chapter-{index:03}.md").write_text(
            f"# Fixture chapter {index}\n\nOffline pagination evidence.\n", encoding="utf-8"
        )
    chapter = snapshot / "reproducible-research" / "testing.md"
    chapter.parent.mkdir()
    chapter.write_text("# Testing\n\nUse repeatable automated tests.\n", encoding="utf-8")
    manifest = tmp_path / "sources.yaml"
    manifest.write_text(
        "sources:\n"
        "  - id: turing-way\n"
        "    title: The Turing Way\n"
        "    repository: the-turing-way/the-turing-way\n"
        "    ref: bb3f7abb56a40cd92a654fb51e4ec91f429cca2a\n"
        "    content_root: book/website\n"
        "    snapshot_path: snapshot\n"
        "    license: CC-BY-4.0\n"
        "    enabled: true\n",
        encoding="utf-8",
    )
    registry = SourceRegistry(manifest, offline=True)
    try:
        yield registry
    finally:
        await registry.close()


def test_repository_fact_accepts_commit_pinned_history_url() -> None:
    fact = RepositoryFact(
        statement="The reviewed commit's reachable history contains one commit.",
        url="https://github.com/example/repository/commits/1234567",
    )

    assert fact.url == "https://github.com/example/repository/commits/1234567"


def test_review_inputs_normalize_area_names() -> None:
    row = TuringWayReviewScoreRow(
        area="Project design",
        score=1,
        claim="The README documents the project purpose and citation.",
        repository_fact={
            "statement": "readme.md is present.",
            "url": "https://github.com/example/repository/blob/1234567/readme.md",
        },
    )
    assert row.area == "project design"


async def test_mcp_contract_in_memory() -> None:
    registry = SourceRegistry(ROOT / "corpus/sources.yaml", offline=True)
    server = create_server(registry)

    async with Client(server) as client:
        tools_result = await client.list_tools()
        names = {tool.name for tool in tools_result.tools}
        assert names == {
            "list_resources",
            "get_resource",
            "list_mygpt_datasets",
            "list_mygpt_documents",
            "query_mygpt_context",
            "get_rag_status",
            "get_turing_way_evidence_packets",
            "get_turing_way_review_evidence",
            "render_validated_turing_way_review",
            "validate_turing_way_review",
        }
        list_tool = next(tool for tool in tools_result.tools if tool.name == "list_resources")
        offset_schema = list_tool.input_schema["properties"]["offset"]
        assert offset_schema["type"] == "integer"
        assert offset_schema["minimum"] == 0
        assert offset_schema["default"] == 0
        assert "offset" not in list_tool.input_schema.get("required", [])

        listed = await client.call_tool("list_resources", {})
        assert listed.structured_content is not None
        entries = listed.structured_content["result"]
        assert entries, "offline snapshot should provide resources"
        assert all(entry["origin"] == "snapshot" for entry in entries)

        document = await client.call_tool(
            "get_resource",
            {"resource_id": entries[0]["resource_id"]},
        )
        assert document.structured_content is not None
        assert document.structured_content["content"].strip()

    await registry.close()


async def test_mygpt_library_tools_return_typed_api_data() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["content-type"] == "application/json"
        if request.url.path == "/api/get_datasets/":
            assert request.content == b'{"user_email":"scientist@example.org","user_group":""}'
            return httpx.Response(200, json=[{"dataset_name": "Turing Way", "dataset_size": 3}])
        if request.url.path == "/api/get_documents/":
            assert request.content == (
                b'{"user_email":"scientist@example.org","user_group":"","dataset":"Turing Way"}'
            )
            return httpx.Response(200, json={"documents": [{"paper_title": "Guide"}]})
        assert request.url.path == "/api/get_context/"
        context_request = json.loads(request.content)
        assert context_request["text"]
        assert context_request["dataset"] in {"Turing Way", "turing-way"}
        assert {
            key: context_request[key]
            for key in (
                "model_type",
                "new_conversation",
                "previous_query",
                "no_context",
                "use_default_qrs",
                "question_best_distance",
                "question_worst_distance",
                "maximum_chunks_count",
                "no_cutoff",
            )
        } == {
            "model_type": "llama3:latest",
            "new_conversation": True,
            "previous_query": "",
            "no_context": False,
            "use_default_qrs": True,
            "question_best_distance": 0.2,
            "question_worst_distance": 1.7,
            "maximum_chunks_count": 5,
            "no_cutoff": False,
        }
        return httpx.Response(
            200,
            json={
                "context": "Keep a record of your workflow.",
                "relevance_score": 61,
                "semantic_score": 58,
                "keyword_score": 42,
                "rerank_score": 0,
                "sources": [{"title": "Turing Way", "url": "https://example.org/source"}],
            },
        )

    mygpt = MyGPTClient(
        MyGPTSettings("https://mygpt.example", model_id="llama3:latest"),
        client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )
    registry = SourceRegistry(ROOT / "corpus/sources.yaml", offline=True)
    resource_id = (await registry.list_resources())[0].id
    server = create_server(registry, mygpt)

    async with Client(server) as client:
        datasets = await client.call_tool(
            "list_mygpt_datasets", {"user_email": "scientist@example.org"}
        )
        assert datasets.structured_content == {
            "result": [{"dataset_name": "Turing Way", "dataset_size": 3}]
        }
        documents = await client.call_tool(
            "list_mygpt_documents",
            {"user_email": "scientist@example.org", "dataset": "Turing Way"},
        )
        assert documents.structured_content == {"result": [{"title": "Guide"}]}
        context = await client.call_tool(
            "query_mygpt_context",
            {
                "question": "How do I make my analysis reproducible?",
                "dataset": "Turing Way",
            },
        )
        assert context.structured_content == {
            "context": "Keep a record of your workflow.",
            "relevance_score": 61.0,
            "semantic_score": 58.0,
            "keyword_score": 42.0,
            "rerank_score": 0.0,
            "sources": [{"title": "Turing Way", "url": "https://example.org/source"}],
        }
        rag_status = await client.call_tool("get_rag_status", {})
        assert rag_status.structured_content == {
            "status": "ready",
            "dataset": "turing-way",
            "model_id": "llama3:latest",
            "relevance_score": 61.0,
            "source_count": 1,
        }
        review_evidence = await client.call_tool("get_turing_way_review_evidence", {})
        assert review_evidence.structured_content is not None
        areas = review_evidence.structured_content["result"]
        assert [area["area"] for area in areas] == [
            "project design",
            "reproducibility",
            "version control and collaboration",
        ]
        assert all(area["retrieval"]["sources"] for area in areas)
        evidence_packets = await client.call_tool(
            "get_turing_way_evidence_packets",
            {
                "requests": [
                    {
                        "claim": "Use a reproducible environment for analysis.",
                        "resource_id": resource_id,
                        "repository_fact": {
                            "statement": "The repository has no environment file.",
                            "url": "https://github.com/example/repository/tree/1234567",
                        },
                    }
                ]
            },
        )
        assert evidence_packets.structured_content is not None
        packet = evidence_packets.structured_content["result"][0]
        assert packet["claim"] == "Use a reproducible environment for analysis."
        assert packet["citation"]["resource_id"] == resource_id
        assert packet["citation"]["title"] == "Project Design"
        assert packet["citation"]["url"].endswith("/book/website/project-design.md")
        assert packet["retrieval"]["relevance_score"] == 61.0
        assert packet["repository_fact"] == {
            "statement": "The repository has no environment file.",
            "url": "https://github.com/example/repository/tree/1234567",
        }
        score_rows = [
            {
                "area": "project design",
                "score": 1,
                "claim": "The project scope is documented.",
                "repository_fact": {
                    "statement": "The README documents the project scope.",
                    "url": "https://github.com/example/repository/blob/1234567/README.md",
                },
            },
            {
                "area": "reproducibility",
                "score": 1,
                "claim": "The repository has a dependency file.",
                "repository_fact": {
                    "statement": "requirements.txt is present.",
                    "url": "https://github.com/example/repository/blob/1234567/requirements.txt",
                },
            },
            {
                "area": "version control and collaboration",
                "score": 0,
                "claim": "The reviewed history has a single commit.",
                "repository_fact": {
                    "statement": "The history has one commit.",
                    "url": "https://github.com/example/repository/commits/1234567",
                },
            },
        ]
        review_validation = await client.call_tool(
            "validate_turing_way_review",
            {"score_rows": score_rows, "recommendations": [packet]},
        )
        assert review_validation.structured_content == {
            "status": "approved",
            "errors": [],
            "total": 2,
            "label": "Developing",
        }
        rendered_review = await client.call_tool(
            "render_validated_turing_way_review",
            {"score_rows": score_rows, "recommendations": [packet]},
        )
        assert rendered_review.structured_content == {
            "status": "approved",
            "errors": [],
            "total": 2,
            "label": "Developing",
            "report": (
                "### Area scores\n\n"
                "**Rating:** Developing (2 / 6)\n\n"
                "| Area | Score | Evidence-backed rationale | Repository evidence |\n"
                "| --- | --- | --- | --- |\n"
                "| Project Design | 1 / 2 | The project scope is documented. | "
                "[Repository evidence](https://github.com/example/repository/blob/"
                "1234567/README.md) |\n"
                "| Reproducibility | 1 / 2 | The repository has a dependency file. | "
                "[Repository evidence](https://github.com/example/repository/blob/"
                "1234567/requirements.txt) |\n"
                "| Version Control And Collaboration | 0 / 2 | "
                "The reviewed history has a single commit. | "
                "[Repository evidence](https://github.com/example/repository/commits/1234567) |\n\n"
                "### Prioritized improvements\n\n"
                "1. **Use a reproducible environment for analysis.**\n"
                "   - **Repository fact:** The repository has no environment file. "
                "([Repository evidence](https://github.com/example/repository/tree/1234567))\n"
                "   - **Turing Way citation:** [Project Design]("
                f"{packet['citation']['url']})\n"
                "   - **MyGPT RAG relevance:** 61%"
            ),
            "score_section": (
                "### Area scores\n\n"
                "**Rating:** Developing (2 / 6)\n\n"
                "| Area | Score | Evidence-backed rationale | Repository evidence |\n"
                "| --- | --- | --- | --- |\n"
                "| Project Design | 1 / 2 | The project scope is documented. | "
                "[Repository evidence](https://github.com/example/repository/blob/"
                "1234567/README.md) |\n"
                "| Reproducibility | 1 / 2 | The repository has a dependency file. | "
                "[Repository evidence](https://github.com/example/repository/blob/"
                "1234567/requirements.txt) |\n"
                "| Version Control And Collaboration | 0 / 2 | "
                "The reviewed history has a single commit. | "
                "[Repository evidence](https://github.com/example/repository/commits/1234567) |"
            ),
            "recommendation_evidence_block": (
                "### Prioritized improvements\n\n"
                "1. **Use a reproducible environment for analysis.**\n"
                "   - **Repository fact:** The repository has no environment file. "
                "([Repository evidence](https://github.com/example/repository/tree/1234567))\n"
                "   - **Turing Way citation:** [Project Design]("
                f"{packet['citation']['url']})\n"
                "   - **MyGPT RAG relevance:** 61%"
            ),
        }
        invalid_fact = await client.call_tool(
            "get_turing_way_evidence_packets",
            {
                "requests": [
                    {
                        "claim": "Use a reproducible environment for analysis.",
                        "resource_id": resource_id,
                        "repository_fact": {
                            "statement": "The repository has no environment file.",
                            "url": "https://example.org/not-a-repository",
                        },
                    }
                ]
            },
        )
        assert invalid_fact.is_error
        unscoped_fact = await client.call_tool(
            "get_turing_way_evidence_packets",
            {
                "requests": [
                    {
                        "claim": "Use a reproducible environment for analysis.",
                        "resource_id": resource_id,
                        "repository_fact": {
                            "statement": "The repository has no environment file.",
                            "url": "https://github.com/example/repository",
                        },
                    }
                ]
            },
        )
        assert unscoped_fact.is_error
        withheld_validation = await client.call_tool(
            "validate_turing_way_review",
            {
                "score_rows": [],
                "recommendations": [{**packet, "repository_fact": None}],
            },
        )
        assert withheld_validation.structured_content == {
            "status": "withheld",
            "errors": [
                "provide exactly one score row for each required review area",
                "recommendation 1 has no repository fact",
            ],
            "total": None,
            "label": None,
        }
        withheld_review = await client.call_tool(
            "render_validated_turing_way_review",
            {
                "score_rows": [],
                "recommendations": [{**packet, "repository_fact": None}],
            },
        )
        assert withheld_review.structured_content == {
            "status": "withheld",
            "errors": [
                "provide exactly one score row for each required review area",
                "recommendation 1 has no repository fact",
            ],
            "total": None,
            "label": None,
            "report": (
                "### Score withheld\n\n"
                "- provide exactly one score row for each required review area\n"
                "- recommendation 1 has no repository fact"
            ),
            "score_section": (
                "### Score withheld\n\n"
                "- provide exactly one score row for each required review area\n"
                "- recommendation 1 has no repository fact"
            ),
            "recommendation_evidence_block": None,
        }
        unknown_resource = await client.call_tool(
            "get_turing_way_evidence_packets",
            {
                "requests": [
                    {
                        "claim": "Use a reproducible environment for analysis.",
                        "resource_id": "turing-way:not-a-resource",
                    }
                ]
            },
        )
        assert unknown_resource.is_error

    await registry.close()


async def test_list_resources_respects_its_limit() -> None:
    registry = SourceRegistry(ROOT / "corpus/sources.yaml", offline=True)
    server = create_server(registry)

    async with Client(server) as client:
        result = await client.call_tool("list_resources", {"limit": 1})
        assert result.structured_content is not None
        assert len(result.structured_content["result"]) == 1

    await registry.close()


async def test_list_resources_pages_without_gaps_and_preserves_metadata(
    paginated_registry: SourceRegistry, monkeypatch: pytest.MonkeyPatch
) -> None:
    records = await paginated_registry.list_resources()
    expected = [
        {
            "resource_id": record.id,
            "title": record.title,
            "path": record.path,
            "url": record.url,
            "origin": record.origin,
        }
        for record in sorted(records, key=lambda record: record.id)
    ]
    assert len(expected) == 405
    server = create_server(paginated_registry)

    async def reversed_records() -> list[ResourceRecord]:
        return list(reversed(records))

    async with Client(server) as client:
        first = await client.call_tool("list_resources", {"limit": 200})
        assert not first.is_error and first.structured_content is not None
        entries = list(first.structured_content["result"])
        assert entries == expected[:200]

        monkeypatch.setattr(paginated_registry, "list_resources", reversed_records)
        for offset, count in ((200, 200), (400, 5), (405, 0), (10000, 0)):
            page = await client.call_tool("list_resources", {"limit": 200, "offset": offset})
            assert not page.is_error
            assert page.structured_content == {"result": expected[offset : offset + 200]}
            assert len(page.structured_content["result"]) == count
            entries.extend(page.structured_content["result"])

        repeated = await client.call_tool("list_resources", {"limit": 200, "offset": 0})
        assert repeated.structured_content == first.structured_content

    assert entries == expected
    assert len({entry["resource_id"] for entry in entries}) == 405


async def test_list_resources_preserves_defaults_and_limit_clamping(
    paginated_registry: SourceRegistry,
) -> None:
    server = create_server(paginated_registry)
    async with Client(server) as client:
        default = await client.call_tool("list_resources", {})
        explicit = await client.call_tool("list_resources", {"limit": 25, "offset": 0})
        assert not default.is_error and default.structured_content is not None
        assert default.structured_content == explicit.structured_content
        assert len(default.structured_content["result"]) == 25

        for limit, count in ((-1, 1), (0, 1), (1, 1), (25, 25), (200, 200), (999, 200)):
            page = await client.call_tool("list_resources", {"limit": limit, "offset": 25})
            assert not page.is_error and page.structured_content is not None
            assert len(page.structured_content["result"]) == count
            assert page.structured_content["result"][0]["resource_id"].endswith("chapter-025")

        exact_end = await client.call_tool("list_resources", {"limit": 5, "offset": 400})
        after_end = await client.call_tool("list_resources", {"limit": 5, "offset": 405})
        assert exact_end.structured_content is not None
        assert len(exact_end.structured_content["result"]) == 5
        assert after_end.structured_content == {"result": []}


async def test_list_resources_returns_typed_empty_pages_for_empty_registry(tmp_path: Path) -> None:
    manifest = tmp_path / "sources.yaml"
    manifest.write_text("sources: []\n", encoding="utf-8")
    registry = SourceRegistry(manifest, offline=True)
    try:
        async with Client(create_server(registry)) as client:
            for arguments in ({}, {"limit": 200, "offset": 0}, {"offset": 10}):
                result = await client.call_tool("list_resources", arguments)
                assert not result.is_error
                assert result.structured_content == {"result": []}
    finally:
        await registry.close()


@pytest.mark.parametrize("offset", [-1, -200, 1.5, "invalid", "1", True, None])
async def test_list_resources_rejects_invalid_offsets(offset: object) -> None:
    registry = SourceRegistry(ROOT / "corpus/sources.yaml", offline=True)
    try:
        async with Client(create_server(registry)) as client:
            result = await client.call_tool("list_resources", {"offset": offset})
            assert result.is_error
            assert any(
                "offset" in block.text for block in result.content if isinstance(block, TextContent)
            )
            valid = await client.call_tool("list_resources", {"limit": 1, "offset": 0})
            assert not valid.is_error and valid.structured_content is not None
            assert len(valid.structured_content["result"]) == 1
    finally:
        await registry.close()


async def test_later_page_resource_can_be_read_and_used_in_evidence_packet(
    paginated_registry: SourceRegistry,
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/get_context/"
        payload = json.loads(request.content)
        assert payload["text"] == "Use repeatable automated tests."
        assert payload["dataset"] == "turing-way"
        return httpx.Response(
            200,
            json={
                "context": "Use repeatable automated tests.",
                "relevance_score": 80,
                "sources": [{"title": "Testing", "url": "https://example.org/testing"}],
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
        mygpt = MyGPTClient(
            MyGPTSettings("https://mygpt.example", model_id="test-model"), client=http_client
        )
        async with Client(create_server(paginated_registry, mygpt)) as client:
            page = await client.call_tool("list_resources", {"limit": 200, "offset": 400})
            assert page.structured_content is not None
            entry = next(
                entry
                for entry in page.structured_content["result"]
                if entry["path"].endswith("/reproducible-research/testing.md")
            )
            document = await client.call_tool("get_resource", {"resource_id": entry["resource_id"]})
            assert not document.is_error and document.structured_content is not None
            assert document.structured_content["content"] == (
                "# Testing\n\nUse repeatable automated tests.\n"
            )
            fact = {
                "statement": "The repository documents how to run tests.",
                "url": "https://github.com/example/repository/blob/1234567/README.md",
            }
            packets = await client.call_tool(
                "get_turing_way_evidence_packets",
                {
                    "requests": [
                        {
                            "claim": "Use repeatable automated tests.",
                            "resource_id": entry["resource_id"],
                            "repository_fact": fact,
                        }
                    ]
                },
            )
            assert not packets.is_error and packets.structured_content is not None
            packet = packets.structured_content["result"][0]
            assert packet["claim"] == "Use repeatable automated tests."
            assert packet["repository_fact"] == fact
            assert packet["citation"] == {
                **entry,
                "repository": "the-turing-way/the-turing-way",
                "ref": "bb3f7abb56a40cd92a654fb51e4ec91f429cca2a",
            }
            assert packet["retrieval"]["relevance_score"] == 80
            assert packet["retrieval"]["context"] == "Use repeatable automated tests."


async def test_unknown_resource_id_is_rejected() -> None:
    registry = SourceRegistry(ROOT / "corpus/sources.yaml", offline=True)
    server = create_server(registry)

    async with Client(server) as client:
        result = await client.call_tool("get_resource", {"resource_id": "turing-way:nope"})
        assert result.is_error

    await registry.close()
