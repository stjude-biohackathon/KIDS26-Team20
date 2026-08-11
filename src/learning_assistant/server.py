"""A deliberately small MCP server: list the corpus, then read one page of it.

This is starting scaffolding, not a finished product. It exists so that on day
one everyone can confirm two things at once: the server is installed and
running, and it can reach GitHub. Ranking, personas, and learning paths are
hackathon work, not inherited code.
"""

from __future__ import annotations

from mcp.server import MCPServer
from starlette.requests import Request
from starlette.responses import JSONResponse

from learning_assistant.models import ResourceDocument, ResourceSummary
from learning_assistant.sources import SourceRegistry

DEFAULT_LIMIT = 25
MAX_LIMIT = 200


def create_server(registry: SourceRegistry | None = None) -> MCPServer:
    source_registry = registry or SourceRegistry.from_environment()
    server = MCPServer(
        "St. Jude AI and Data Learning Assistant",
        instructions=(
            "Use list_resources to see what is available, then get_resource to read one "
            "page in full. Cite the returned source URL. Do not invent institutional "
            "policy or claim that public guidance is St. Jude policy."
        ),
    )

    @server.custom_route("/health", methods=["GET"], include_in_schema=False)
    async def health(_request: Request) -> JSONResponse:
        """Report process health without invoking an MCP tool."""
        return JSONResponse({"status": "ok"})

    @server.tool()
    async def list_resources(limit: int = DEFAULT_LIMIT) -> list[ResourceSummary]:
        """List available resources. Each entry's origin is 'github' or 'snapshot'."""
        records = await source_registry.list_resources()
        capped = max(1, min(limit, MAX_LIMIT))
        return [
            ResourceSummary(
                resource_id=record.id,
                title=record.title,
                path=record.path,
                url=record.url,
                origin=record.origin,
            )
            for record in records[:capped]
        ]

    @server.tool()
    async def get_resource(resource_id: str) -> ResourceDocument:
        """Read one complete resource, using a resource_id from list_resources."""
        document = await source_registry.get_document(resource_id)
        if document is None:
            raise ValueError(f"unknown resource_id: {resource_id}")
        return document

    return server


mcp = create_server()
