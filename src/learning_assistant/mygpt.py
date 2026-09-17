"""Read-only client for a separately deployed MyGPT library API."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from urllib.parse import urlsplit

import httpx

from learning_assistant.models import (
    MyGPTContext,
    MyGPTDataset,
    MyGPTDocument,
    RAGStatus,
    TuringWayReviewEvidence,
)


class MyGPTConfigurationError(ValueError):
    """Raised when the optional MyGPT service URL is not safe to use."""


class MyGPTRequestError(RuntimeError):
    """Raised when MyGPT cannot provide a usable response."""


@dataclass(frozen=True)
class MyGPTSettings:
    base_url: str
    model_id: str | None = None

    @classmethod
    def from_environment(cls, environment: Mapping[str, str] | None = None) -> MyGPTSettings:
        values = environment if environment is not None else os.environ
        base_url = values.get("MYGPT_BASE_URL", "").strip().rstrip("/")
        if not base_url:
            raise MyGPTConfigurationError(
                "MyGPT is not configured. Set MYGPT_BASE_URL to the approved MyGPT API URL."
            )
        parsed = urlsplit(base_url)
        local_http = parsed.scheme == "http" and parsed.hostname in {
            "localhost",
            "127.0.0.1",
            "host.docker.internal",
            "mygpt-backend",
        }
        if (parsed.scheme != "https" and not local_http) or not parsed.hostname:
            raise MyGPTConfigurationError(
                "MYGPT_BASE_URL must be HTTPS, or HTTP on an approved local host."
            )
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise MyGPTConfigurationError(
                "MYGPT_BASE_URL must not contain credentials, a query string, or a fragment."
            )
        model_id = values.get("MYGPT_MODEL_ID", "").strip() or None
        return cls(base_url=base_url, model_id=model_id)


class MyGPTClient:
    """Call MyGPT's documented, read-only library endpoints."""

    def __init__(
        self,
        settings: MyGPTSettings | None = None,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings
        self._client = client or httpx.AsyncClient(timeout=20.0)
        self._owns_client = client is None

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def list_datasets(self, user_email: str) -> list[MyGPTDataset]:
        payload = await self._post("/api/get_datasets/", user_email)
        if not isinstance(payload, list):
            raise MyGPTRequestError("MyGPT returned an invalid dataset response.")
        try:
            return [MyGPTDataset.model_validate(item) for item in payload]
        except (TypeError, ValueError) as error:
            raise MyGPTRequestError("MyGPT returned an invalid dataset record.") from error

    async def list_documents(self, user_email: str, dataset: str) -> list[MyGPTDocument]:
        payload = await self._post("/api/get_documents/", user_email, dataset=dataset)
        if not isinstance(payload, dict) or not isinstance(payload.get("documents"), list):
            raise MyGPTRequestError("MyGPT returned an invalid document response.")
        try:
            return [
                MyGPTDocument.model_validate({"title": document["paper_title"]})
                for document in payload["documents"]
            ]
        except (KeyError, TypeError, ValueError) as error:
            raise MyGPTRequestError("MyGPT returned an invalid document record.") from error

    async def query_context(self, question: str, dataset: str) -> MyGPTContext:
        settings = self.settings or MyGPTSettings.from_environment()
        if not settings.model_id:
            raise MyGPTConfigurationError(
                "MyGPT question retrieval requires MYGPT_MODEL_ID to be configured."
            )
        payload = await self._request(
            "/api/get_context/",
            {
                "text": question,
                "model_type": settings.model_id,
                "dataset": dataset,
                "new_conversation": True,
                "previous_query": "",
                "no_context": False,
                "use_default_qrs": True,
                "question_best_distance": 0.2,
                "question_worst_distance": 1.7,
                "maximum_chunks_count": 5,
                "no_cutoff": False,
            },
        )
        if not isinstance(payload, dict):
            raise MyGPTRequestError("MyGPT returned an invalid context response.")
        try:
            return MyGPTContext.model_validate(payload)
        except ValueError as error:
            raise MyGPTRequestError("MyGPT returned invalid context data.") from error

    async def review_evidence(self) -> list[TuringWayReviewEvidence]:
        """Retrieve required RAG evidence for every Turing Way review area."""
        queries = {
            "project design": (
                "research software project design documentation scope structure "
                "and maintainability best practices"
            ),
            "reproducibility": (
                "reproducible research dependency management environments data "
                "access automation and testing best practices"
            ),
            "version control and collaboration": (
                "research software version control commit history contribution "
                "guidelines collaboration and code review best practices"
            ),
        }
        return [
            TuringWayReviewEvidence(
                area=area,
                query=query,
                retrieval=await self.query_context(query, "turing-way"),
            )
            for area, query in queries.items()
        ]

    async def claim_evidence(self, claims: list[str]) -> list[TuringWayReviewEvidence]:
        """Retrieve MyGPT RAG evidence for specific review recommendations."""
        if not 1 <= len(claims) <= 5:
            raise ValueError("provide between one and five review claims")
        if any(not claim.strip() for claim in claims):
            raise ValueError("review claims must not be empty")
        return [
            TuringWayReviewEvidence(
                area=f"claim {position}",
                query=claim,
                retrieval=await self.query_context(claim, "turing-way"),
            )
            for position, claim in enumerate(claims, start=1)
        ]

    async def rag_status(self) -> RAGStatus:
        """Confirm that the configured model can retrieve Turing Way evidence."""
        settings = self.settings or MyGPTSettings.from_environment()
        if not settings.model_id:
            raise MyGPTConfigurationError(
                "MyGPT RAG status requires MYGPT_MODEL_ID to be configured."
            )
        retrieval = await self.query_context(
            "What is The Turing Way and how does it support reproducible research?",
            "turing-way",
        )
        source_count = len(retrieval.sources)
        if source_count == 0:
            raise MyGPTRequestError(
                "MyGPT returned no Turing Way sources; the RAG dataset is not ready."
            )
        return RAGStatus(
            status="ready",
            dataset="turing-way",
            model_id=settings.model_id,
            relevance_score=retrieval.relevance_score,
            source_count=source_count,
        )

    async def _post(self, path: str, user_email: str, **data: str) -> object:
        return await self._request(path, {"user_email": user_email, "user_group": "", **data})

    async def _request(self, path: str, payload: dict[str, object]) -> object:
        settings = self.settings or MyGPTSettings.from_environment()
        try:
            response = await self._client.post(
                f"{settings.base_url}{path}",
                json=payload,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            raise MyGPTRequestError(
                f"MyGPT request failed with HTTP status {error.response.status_code}."
            ) from error
        except httpx.HTTPError as error:
            raise MyGPTRequestError("MyGPT could not be reached. Check MYGPT_BASE_URL.") from error
        try:
            return response.json()
        except ValueError as error:
            raise MyGPTRequestError("MyGPT returned invalid JSON.") from error
