"""A deliberately small MCP server: list the corpus, then read one page of it.

This is starting scaffolding, not a finished product. It exists so that on day
one everyone can confirm two things at once: the server is installed and
running, and it can reach GitHub. Ranking, personas, and learning paths are
hackathon work, not inherited code.
"""

from __future__ import annotations

from typing import Annotated

from mcp.server import MCPServer
from pydantic import Field
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
    TuringWayReviewRender,
    TuringWayReviewScoreRow,
    TuringWayReviewValidation,
)
from learning_assistant.mygpt import MyGPTClient
from learning_assistant.sources import SourceRegistry

DEFAULT_LIMIT = 25
MAX_LIMIT = 200


def validate_turing_way_review_inputs(
    score_rows: list[TuringWayReviewScoreRow],
    recommendations: list[TuringWayEvidencePacket],
) -> TuringWayReviewValidation:
    """Calculate a score only when the complete review report contract is met."""
    expected_areas = {
        "project design",
        "reproducibility",
        "version control and collaboration",
    }
    errors: list[str] = []
    areas = [row.area for row in score_rows]
    if len(score_rows) != 3 or set(areas) != expected_areas or len(set(areas)) != len(areas):
        errors.append("provide exactly one score row for each required review area")
    if not 1 <= len(recommendations) <= 5:
        errors.append("provide between one and five recommendation evidence packets")
    for index, packet in enumerate(recommendations, start=1):
        if packet.repository_fact is None:
            errors.append(f"recommendation {index} has no repository fact")
        if packet.retrieval.relevance_score is None:
            errors.append(f"recommendation {index} has no MyGPT relevance score")

    if errors:
        return TuringWayReviewValidation(status="withheld", errors=errors)

    total = sum(row.score for row in score_rows)
    label = (
        "Starting"
        if total <= 1
        else "Developing"
        if total <= 3
        else "Established"
        if total <= 5
        else "Strong foundation"
    )
    return TuringWayReviewValidation(status="approved", total=total, label=label)


def markdown_table_cell(value: str) -> str:
    """Render a single line Markdown table cell from observed text."""
    return " ".join(value.split()).replace("|", r"\|")


def format_relevance_score(relevance_score: float) -> str:
    """Format the MyGPT-provided relevance value as a percentage."""
    return f"{relevance_score:g}%"


def render_validated_turing_way_review_sections(
    score_rows: list[TuringWayReviewScoreRow],
    recommendations: list[TuringWayEvidencePacket],
    validation: TuringWayReviewValidation,
) -> TuringWayReviewRender:
    """Build canonical report sections from validated review inputs."""
    if validation.status != "approved":
        errors = "\n".join(f"- {error}" for error in validation.errors)
        score_section = f"### Score withheld\n\n{errors}"
        return TuringWayReviewRender(
            status=validation.status,
            errors=validation.errors,
            report=score_section,
            score_section=score_section,
        )

    score_rows_by_area = {row.area: row for row in score_rows}
    area_order = (
        "project design",
        "reproducibility",
        "version control and collaboration",
    )
    score_lines = [
        "### Area scores",
        "",
        f"**Rating:** {validation.label} ({validation.total} / 6)",
        "",
        "| Area | Score | Evidence-backed rationale | Repository evidence |",
        "| --- | --- | --- | --- |",
    ]
    for area in area_order:
        row = score_rows_by_area[area]
        score_lines.append(
            f"| {row.area.title()} | {row.score} / 2 | {markdown_table_cell(row.claim)} | "
            f"[Repository evidence]({row.repository_fact.url}) |"
        )

    recommendation_lines = ["### Prioritized improvements", ""]
    for index, packet in enumerate(recommendations, start=1):
        repository_fact = packet.repository_fact
        assert repository_fact is not None
        relevance_score = packet.retrieval.relevance_score
        assert relevance_score is not None
        recommendation_lines.extend(
            [
                f"{index}. **{markdown_table_cell(packet.claim)}**",
                (
                    f"   - **Repository fact:** {markdown_table_cell(repository_fact.statement)} "
                    f"([Repository evidence]({repository_fact.url}))"
                ),
                (
                    f"   - **Turing Way citation:** "
                    f"[{markdown_table_cell(packet.citation.title)}]({packet.citation.url})"
                ),
                (f"   - **MyGPT RAG relevance:** {format_relevance_score(relevance_score)}"),
            ]
        )

    score_section = "\n".join(score_lines)
    recommendation_evidence_block = "\n".join(recommendation_lines)
    return TuringWayReviewRender(
        status=validation.status,
        errors=validation.errors,
        total=validation.total,
        label=validation.label,
        report=f"{score_section}\n\n{recommendation_evidence_block}",
        score_section=score_section,
        recommendation_evidence_block=recommendation_evidence_block,
    )


def create_server(
    registry: SourceRegistry | None = None, mygpt_client: MyGPTClient | None = None
) -> MCPServer:
    source_registry = registry or SourceRegistry.from_environment()
    mygpt = mygpt_client or MyGPTClient()
    server = MCPServer(
        "St. Jude AI and Data Learning Assistant",
        instructions=(
            "Use list_resources to see what is available, then get_resource to read one "
            "page in full. For discovery, use limit=200 and offset=0, then advance offset "
            "by the number of entries returned until the needed resources are found or "
            "a page has fewer than 200 entries. Cite the returned source URL. "
            "Do not invent institutional "
            "policy or claim that public guidance is St. Jude policy."
        ),
    )

    @server.custom_route("/health", methods=["GET"], include_in_schema=False)
    async def health(_request: Request) -> JSONResponse:
        """Report process health without invoking an MCP tool."""
        return JSONResponse({"status": "ok"})

    @server.tool()
    async def list_resources(
        limit: int = DEFAULT_LIMIT,
        offset: Annotated[int, Field(ge=0, strict=True)] = 0,
    ) -> list[ResourceSummary]:
        """List resources sorted by resource ID, starting at zero-based offset.

        Limit defaults to 25 and is clamped to 1-200. Advance offset by the
        number of entries returned; a page shorter than the effective limit
        ends the listing. Offsets at or beyond the end return an empty list.
        Each entry's origin is 'github' or 'snapshot'.
        """
        records = sorted(await source_registry.list_resources(), key=lambda record: record.id)
        capped = max(1, min(limit, MAX_LIMIT))
        return [
            ResourceSummary(
                resource_id=record.id,
                title=record.title,
                path=record.path,
                url=record.url,
                origin=record.origin,
            )
            for record in records[offset : offset + capped]
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

    @server.tool()
    async def validate_turing_way_review(
        score_rows: list[TuringWayReviewScoreRow],
        recommendations: list[TuringWayEvidencePacket],
    ) -> TuringWayReviewValidation:
        """Calculate a review score only when supplied evidence packets meet the report contract."""
        return validate_turing_way_review_inputs(score_rows, recommendations)

    @server.tool()
    async def render_validated_turing_way_review(
        score_rows: list[TuringWayReviewScoreRow],
        recommendations: list[TuringWayEvidencePacket],
    ) -> TuringWayReviewRender:
        """Validate and render a review without rewriting evidence."""
        validation = validate_turing_way_review_inputs(score_rows, recommendations)
        return render_validated_turing_way_review_sections(score_rows, recommendations, validation)

    return server


mcp = create_server()
