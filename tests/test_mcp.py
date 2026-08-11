from pathlib import Path

from mcp import Client

from learning_assistant.server import create_server
from learning_assistant.sources import SourceRegistry

ROOT = Path(__file__).resolve().parents[1]


async def test_mcp_contract_in_memory() -> None:
    registry = SourceRegistry(ROOT / "corpus/sources.yaml", offline=True)
    server = create_server(registry)

    async with Client(server) as client:
        tools_result = await client.list_tools()
        names = {tool.name for tool in tools_result.tools}
        assert names == {"list_resources", "get_resource"}

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
