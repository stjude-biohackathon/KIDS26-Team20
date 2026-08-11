"""Load approved Markdown resources from GitHub, with a local snapshot fallback."""

from __future__ import annotations

import os
import re
from pathlib import Path

import httpx
import yaml

from learning_assistant.models import (
    ResourceDocument,
    ResourceRecord,
    SourceConfig,
    SourcesFile,
    resolve_snapshot_path,
)


class SourceRegistry:
    """Registry of configured resource sources with lazy GitHub access."""

    def __init__(
        self,
        config_path: Path,
        *,
        github_token: str | None = None,
        offline: bool = False,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.config_path = config_path.resolve()
        raw_config = yaml.safe_load(self.config_path.read_text(encoding="utf-8"))
        parsed = SourcesFile.model_validate(raw_config)
        self.sources = {source.id: source for source in parsed.sources if source.enabled}
        self.offline = offline
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "stjude-learning-assistant/0.1",
        }
        if github_token:
            headers["Authorization"] = f"Bearer {github_token}"
        self._client = client or httpx.AsyncClient(headers=headers, timeout=30.0)
        self._owns_client = client is None
        self._records: dict[str, ResourceRecord] = {}
        self._loaded = False

    @classmethod
    def from_environment(cls) -> SourceRegistry:
        repository_config = Path.cwd() / "corpus/sources.yaml"
        package_config = Path(__file__).resolve().parents[2] / "corpus/sources.yaml"
        default_config = repository_config if repository_config.exists() else package_config
        config_path = Path(os.environ.get("LEARNING_ASSISTANT_SOURCES", default_config))
        offline = os.environ.get("LEARNING_ASSISTANT_OFFLINE", "false").lower() in {
            "1",
            "true",
            "yes",
        }
        return cls(
            config_path,
            github_token=os.environ.get("GITHUB_TOKEN"),
            offline=offline,
        )

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def list_resources(self) -> list[ResourceRecord]:
        if not self._loaded:
            await self.refresh()
        return list(self._records.values())

    async def refresh(self) -> int:
        records: dict[str, ResourceRecord] = {}
        for source in self.sources.values():
            source_records = await self._load_source(source)
            records.update({record.id: record for record in source_records})
        self._records = records
        self._loaded = True
        return len(records)

    async def get_document(self, resource_id: str) -> ResourceDocument | None:
        if not self._loaded:
            await self.refresh()
        record = self._records.get(resource_id)
        if record is None:
            return None
        source = self.sources[record.source_id]
        content = record.content
        if content is None:
            content = await self._fetch_raw(source, record.path)
            record.content = content
        return ResourceDocument(
            resource_id=record.id,
            title=record.title,
            path=record.path,
            url=record.url,
            origin=record.origin,
            repository=source.repository,
            ref=source.ref,
            content=content,
        )

    async def _load_source(self, source: SourceConfig) -> list[ResourceRecord]:
        if self.offline:
            return self._load_snapshot(source) if source.snapshot_path else []
        try:
            return await self._list_github_markdown(source)
        except httpx.HTTPError:
            # Falling back keeps a demonstration working on a bad network. The
            # origin field records which path was actually taken.
            if source.snapshot_path:
                return self._load_snapshot(source)
            raise

    def _load_snapshot(self, source: SourceConfig) -> list[ResourceRecord]:
        snapshot_root = resolve_snapshot_path(self.config_path, source.snapshot_path or "")
        if not snapshot_root.exists():
            raise FileNotFoundError(f"snapshot for {source.id} does not exist: {snapshot_root}")
        records: list[ResourceRecord] = []
        for markdown_file in _snapshot_markdown_files(snapshot_root):
            relative_path = markdown_file.relative_to(snapshot_root).as_posix()
            path_parts = (source.content_root, relative_path)
            repository_path = "/".join(part for part in path_parts if part)
            content = markdown_file.read_text(encoding="utf-8")
            records.append(self._record(source, repository_path, "snapshot", content))
        return records

    async def _list_github_markdown(self, source: SourceConfig) -> list[ResourceRecord]:
        url = f"https://api.github.com/repos/{source.repository}/git/trees/{source.ref}"
        response = await self._client.get(url, params={"recursive": "1"})
        response.raise_for_status()
        tree = response.json().get("tree", [])
        prefix = f"{source.content_root.rstrip('/')}/" if source.content_root else ""
        paths = [
            entry["path"]
            for entry in tree
            if entry.get("type") == "blob"
            and entry.get("path", "").startswith(prefix)
            and entry.get("path", "").lower().endswith(".md")
        ]
        return [self._record(source, path, "github") for path in paths]

    async def _fetch_raw(self, source: SourceConfig, path: str) -> str:
        if self.offline:
            message = f"resource {source.id}:{path} is not present in the offline snapshot"
            raise RuntimeError(message)
        url = f"https://raw.githubusercontent.com/{source.repository}/{source.ref}/{path}"
        response = await self._client.get(url)
        response.raise_for_status()
        return response.text

    def _record(
        self,
        source: SourceConfig,
        path: str,
        origin: str,
        content: str | None = None,
    ) -> ResourceRecord:
        resource_id = f"{source.id}:{path.removesuffix('.md')}"
        title = _extract_title(content) if content else _title_from_path(path)
        url = (
            f"{source.web_url.rstrip('/')}/{path}"
            if source.web_url
            else f"https://github.com/{source.repository}/blob/{source.ref}/{path}"
        )
        return ResourceRecord(
            id=resource_id,
            source_id=source.id,
            title=title,
            path=path,
            url=url,
            origin=origin,
            content=content,
        )


def _extract_title(content: str | None) -> str:
    if content:
        match = re.search(r"(?m)^#\s+(.+?)\s*$", content)
        if match:
            return match.group(1).strip()
    return "Untitled resource"


def _title_from_path(path: str) -> str:
    return Path(path).stem.replace("-", " ").replace("_", " ").title()


def _snapshot_markdown_files(snapshot_root: Path) -> list[Path]:
    markdown_files: list[Path] = []
    for directory, directory_names, file_names in os.walk(snapshot_root, followlinks=False):
        paths = [Path(directory) / name for name in [*directory_names, *file_names]]
        linked_paths = [path for path in paths if _is_link(path)]
        if linked_paths:
            relative_path = linked_paths[0].relative_to(snapshot_root)
            raise ValueError(
                f"snapshot cannot contain symbolic links or junctions: {relative_path}"
            )
        markdown_files.extend(
            Path(directory) / name for name in file_names if name.lower().endswith(".md")
        )
    return sorted(markdown_files)


def _is_link(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or (is_junction is not None and is_junction())
