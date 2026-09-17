import json
from pathlib import Path

import httpx
from mcp import Client

from learning_assistant.mygpt import MyGPTClient, MyGPTSettings
from learning_assistant.server import create_server
from learning_assistant.sources import SourceRegistry

ROOT = Path(__file__).resolve().parents[1]


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
        }

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


async def test_unknown_resource_id_is_rejected() -> None:
    registry = SourceRegistry(ROOT / "corpus/sources.yaml", offline=True)
    server = create_server(registry)

    async with Client(server) as client:
        result = await client.call_tool("get_resource", {"resource_id": "turing-way:nope"})
        assert result.is_error

    await registry.close()
