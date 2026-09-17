"""Typed configuration and MCP result models."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

from pydantic import BaseModel, field_validator

GITHUB_REPOSITORY_PATTERN = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?/[A-Za-z0-9._-]{1,100}"
)
FORBIDDEN_REF_CHARACTERS = frozenset(" ~^:?*[\\#%")


class SourceConfig(BaseModel):
    """A GitHub-backed or local snapshot learning-resource source."""

    id: str
    title: str
    repository: str
    ref: str = "main"
    content_root: str = ""
    snapshot_path: str | None = None
    web_url: str | None = None
    license: str | None = None
    enabled: bool = True

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        allowed_characters = "abcdefghijklmnopqrstuvwxyz0123456789-"
        if not value or any(character not in allowed_characters for character in value):
            raise ValueError("source id must use lowercase letters, digits, and hyphens")
        return value

    @field_validator("repository")
    @classmethod
    def validate_repository(cls, value: str) -> str:
        if not GITHUB_REPOSITORY_PATTERN.fullmatch(value):
            raise ValueError("repository must use the GitHub owner/repository format")
        if value.rsplit("/", 1)[1] in {".", ".."}:
            raise ValueError("repository name cannot be '.' or '..'")
        return value

    @field_validator("ref")
    @classmethod
    def validate_ref(cls, value: str) -> str:
        invalid = (
            not value
            or value.startswith(("/", "."))
            or value.endswith(("/", "."))
            or ".." in value
            or "//" in value
            or "@{" in value
            or value.endswith(".lock")
            or any(character in FORBIDDEN_REF_CHARACTERS for character in value)
            or any(ord(character) < 32 or ord(character) == 127 for character in value)
        )
        if invalid:
            raise ValueError("ref must be a safe Git reference")
        return value

    @field_validator("content_root")
    @classmethod
    def validate_content_root(cls, value: str) -> str:
        parts = value.split("/")
        if (
            value.startswith("/")
            or value.endswith("/")
            or "\\" in value
            or any(part in {".", ".."} for part in parts)
        ):
            raise ValueError("content_root must be a relative POSIX path")
        return value

    @field_validator("web_url")
    @classmethod
    def validate_web_url(cls, value: str | None) -> str | None:
        if value is None:
            return value
        parsed = urlsplit(value)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("web_url must be an HTTPS URL without embedded credentials")
        return value


class ResourceRecord(BaseModel):
    """One resource, as held internally by the registry."""

    id: str
    source_id: str
    title: str
    path: str
    url: str
    # "github" when listed from the GitHub API, "snapshot" when read from disk.
    origin: str
    content: str | None = None


class ResourceSummary(BaseModel):
    """One entry returned by list_resources."""

    resource_id: str
    title: str
    path: str
    url: str
    origin: str


class ResourceDocument(BaseModel):
    """One complete resource returned by get_resource."""

    resource_id: str
    title: str
    path: str
    url: str
    origin: str
    repository: str
    ref: str
    content: str


class MyGPTDataset(BaseModel):
    """A dataset returned by the MyGPT library API."""

    dataset_name: str
    dataset_size: int | None = None


class MyGPTDocument(BaseModel):
    """A document title returned by the MyGPT library API."""

    title: str


class MyGPTContext(BaseModel):
    """Retrieved evidence and scores returned by MyGPT for a question."""

    context: str
    relevance_score: float | None = None
    semantic_score: float | None = None
    keyword_score: float | None = None
    rerank_score: float | None = None
    sources: list[dict[str, object]] = []


class TuringWayReviewEvidence(BaseModel):
    """MyGPT RAG evidence required for one Turing Way review area."""

    area: str
    query: str
    retrieval: MyGPTContext


class RAGStatus(BaseModel):
    """Result of a live retrieval probe for the local Turing Way RAG service."""

    status: str
    dataset: str
    model_id: str
    relevance_score: float | None = None
    source_count: int


class RepositoryFact(BaseModel):
    """An observed repository fact with its public GitHub evidence URL."""

    statement: str
    url: str

    @field_validator("statement")
    @classmethod
    def validate_statement(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("repository fact statement must not be empty")
        return value.strip()

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        parsed = urlsplit(value)
        path_parts = [part for part in parsed.path.split("/") if part]
        if (
            parsed.scheme != "https"
            or parsed.hostname != "github.com"
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or len(path_parts) < 2
        ):
            raise ValueError("repository fact URL must be a public GitHub HTTPS URL")
        return value


class TuringWayEvidenceRequest(BaseModel):
    """One claim that needs a resolved source and a targeted RAG retrieval."""

    claim: str
    resource_id: str
    repository_fact: RepositoryFact | None = None

    @field_validator("claim")
    @classmethod
    def validate_claim(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("evidence claim must not be empty")
        return value.strip()


class ResolvedTuringWayCitation(BaseModel):
    """Pinned, server-resolved citation data safe for final answer rendering."""

    resource_id: str
    title: str
    path: str
    url: str
    repository: str
    ref: str
    origin: str


class TuringWayEvidencePacket(BaseModel):
    """Citation-safe evidence for one final recommendation or checklist action."""

    claim: str
    citation: ResolvedTuringWayCitation
    retrieval: MyGPTContext
    repository_fact: RepositoryFact | None = None


class SourcesFile(BaseModel):
    sources: list[SourceConfig]


def resolve_snapshot_path(config_file: Path, snapshot_path: str) -> Path:
    """Resolve snapshot paths relative to the source configuration file."""
    config_directory = config_file.parent.resolve()
    resolved_path = (config_directory / snapshot_path).resolve()
    try:
        resolved_path.relative_to(config_directory)
    except ValueError as error:
        raise ValueError(
            "snapshot_path must stay within the source configuration directory"
        ) from error
    return resolved_path
