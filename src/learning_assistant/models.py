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
