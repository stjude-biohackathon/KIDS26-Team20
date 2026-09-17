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

from learning_assistant.models import (
    MyGPTContext,
    MyGPTDataset,
    MyGPTDocument,
    RAGStatus,
    ResolvedTuringWayCitation,
    ResourceDocument,
    ResourceSummary,
    TuringWayEvidencePacket,
    TuringWayEvidenceRequest,
    TuringWayReviewEvidence,
)
from learning_assistant.mygpt import MyGPTClient
from learning_assistant.sources import SourceRegistry

DEFAULT_LIMIT = 25
MAX_LIMIT = 200


def create_server(
    registry: SourceRegistry | None = None, mygpt_client: MyGPTClient | None = None
) -> MCPServer:
    source_registry = registry or SourceRegistry.from_environment()
    mygpt = mygpt_client or MyGPTClient()
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

    @server.tool()
    async def list_mygpt_datasets(user_email: str) -> list[MyGPTDataset]:
        """List the caller's datasets from an approved MyGPT deployment."""
        return await mygpt.list_datasets(user_email)

    @server.tool()
    async def list_mygpt_documents(user_email: str, dataset: str) -> list[MyGPTDocument]:
        """List document titles from one of the caller's MyGPT datasets."""
        return await mygpt.list_documents(user_email, dataset)

    @server.tool()
    async def query_mygpt_context(question: str, dataset: str) -> MyGPTContext:
        """Retrieve MyGPT evidence and cited source records for a question and dataset."""
        return await mygpt.query_context(question, dataset)

    @server.tool()
    async def get_rag_status() -> RAGStatus:
        """Verify that MyGPT can retrieve Turing Way evidence with the configured model."""
        return await mygpt.rag_status()

    @server.tool()
    async def get_turing_way_review_evidence() -> list[TuringWayReviewEvidence]:
        """Run the required MyGPT RAG queries for a Turing Way repository review."""
        return await mygpt.review_evidence()

    @server.tool()
    async def get_turing_way_evidence_packets(
        requests: list[TuringWayEvidenceRequest],
    ) -> list[TuringWayEvidencePacket]:
        """Resolve cited Turing Way chapters and run one matching RAG query per claim."""
        if not 1 <= len(requests) <= 5:
            raise ValueError("provide between one and five evidence requests")
        documents = []
        for request in requests:
            document = await source_registry.get_document(request.resource_id)
            if document is None:
                raise ValueError(f"unknown resource_id: {request.resource_id}")
            documents.append(document)
        retrievals = await mygpt.claim_evidence([request.claim for request in requests])
        return [
            TuringWayEvidencePacket(
                claim=request.claim,
                citation=ResolvedTuringWayCitation(
                    resource_id=document.resource_id,
                    title=document.title,
                    path=document.path,
                    url=document.url,
                    repository=document.repository,
                    ref=document.ref,
                    origin=document.origin,
                ),
                retrieval=evidence.retrieval,
                repository_fact=request.repository_fact,
            )
            for request, document, evidence in zip(requests, documents, retrievals, strict=True)
        ]

    return server


mcp = create_server()
