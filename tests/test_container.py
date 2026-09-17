import importlib.util
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_bootstrap_module():
    spec = importlib.util.spec_from_file_location(
        "bootstrap_mygpt_dataset", ROOT / "scripts/bootstrap_mygpt_dataset.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_compose_runs_the_live_server_on_loopback_only() -> None:
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text(encoding="utf-8"))
    service = compose["services"]["learning-assistant"]

    assert service["build"]["context"] == "."
    assert service["environment"]["LEARNING_ASSISTANT_OFFLINE"] == "false"
    assert service["environment"]["LEARNING_ASSISTANT_SOURCES"] == "corpus/sources.yaml"
    assert service["environment"]["MYGPT_BASE_URL"] == "http://mygpt-backend:8000"
    assert service["environment"]["MYGPT_MODEL_ID"] == "${MYGPT_MODEL_ID:-qwen2.5:3b}"
    assert service["ports"] == ["127.0.0.1:${LEARNING_ASSISTANT_HOST_PORT:-8000}:8000"]
    assert service["read_only"] is True
    assert service["cap_drop"] == ["ALL"]
    assert service["depends_on"]["mygpt-backend"]["condition"] == "service_healthy"


def test_compose_builds_mygpt_from_a_pinned_upstream_revision() -> None:
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text(encoding="utf-8"))
    backend = compose["services"]["mygpt-backend"]

    assert (
        backend["build"]["context"]
        == "https://github.com/stjude/MyGPT.git#dde3bd762e03a394157a59fe146a4b07c119ecde:backend"
    )
    assert backend["env_file"] == ["config/mygpt.env"]
    assert backend["ports"] == ["127.0.0.1:${MYGPT_BACKEND_HOST_PORT:-8001}:8000"]
    assert (ROOT / "config/mygpt.env.example").is_file()


def test_container_keeps_provider_settings_outside_the_image() -> None:
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    dockerignore = (ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()

    assert "config/workbench.env" in dockerignore
    assert "AIMAAS_" not in dockerfile
    assert '["learning-assistant", "http", "--host", "0.0.0.0", "--port", "8000"]' in dockerfile


def test_docker_documentation_explains_local_mcp_and_mygpt_boundary() -> None:
    text = (ROOT / "docs/DOCKER.md").read_text(encoding="utf-8")

    assert "docker compose up --build" in text
    assert "http://127.0.0.1:8000/mcp" in text
    assert "http://127.0.0.1:8001" in text
    assert "does not call a model" in text
    assert "MyGPT" in text


def test_mygpt_bootstrap_settings_pin_a_safe_turing_way_embedding_configuration() -> None:
    data = yaml.safe_load((ROOT / "config/mygpt-bootstrap.yaml").read_text(encoding="utf-8"))
    dataset = data["dataset"]
    provenance = data["provenance"]

    assert dataset["name"] == "turing-way"
    assert dataset["source_manifest"] == "corpus/sources.yaml"
    assert dataset["chat_model"] == "qwen2.5:3b"
    assert dataset["embedding_model"] == "nomic-embed-text"
    assert dataset["embedding_source"] == "ollama"
    assert dataset["use_bm25"] is True
    assert provenance["source"] == {
        "repository": "the-turing-way/the-turing-way",
        "ref": "bb3f7abb56a40cd92a654fb51e4ec91f429cca2a",
        "content_root": "book/website",
    }
    assert provenance["expected_document_count"] == 487
    assert provenance["minimum_chunk_count"] >= 1


def test_mygpt_bootstrap_skips_only_a_compatible_live_dataset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bootstrap = load_bootstrap_module()
    dataset = {
        "name": "turing-way",
        "chat_model": "qwen2.5:3b",
        "embedding_model": "nomic-embed-text",
        "chunk_size": 1000,
        "chunking_method": "fixed_chunk_size",
        "use_overlap": True,
        "use_bm25": True,
        "documents_language": "english",
        "distance_function": "l2",
    }
    provenance = {"minimum_chunk_count": 1}
    paths = ["book/website/a.md", "book/website/b.md"]
    calls: list[str] = []

    def fake_request(url: str, payload: dict[str, object]) -> object:
        calls.append(url)
        if url.endswith("/api/get_datasets/"):
            return [{"dataset_name": "turing-way", "dataset_size": 12}]
        if url.endswith("/api/get_dataset_details/"):
            return {
                "embedding_model": "nomic-embed-text",
                "chunksize": 1000,
                "chunking_method": "fixed_chunk_size",
                "overlap": True,
                "use_bm25": True,
                "reranker": "None",
                "documents_language": "english",
                "distance_function": "l2",
                "dataset_size": 12,
            }
        if url.endswith("/api/get_documents/"):
            return {"documents": [{"paper_title": path} for path in paths]}
        if url.endswith("/api/get_context/"):
            return {"sources": [{"document": paths[0]}]}
        raise AssertionError(f"unexpected request: {url}")

    monkeypatch.setattr(bootstrap, "request_json", fake_request)

    assert bootstrap.existing_dataset_is_compatible(dataset, provenance, paths) is True
    assert [call.rsplit("/", 2)[-2] for call in calls] == [
        "get_datasets",
        "get_dataset_details",
        "get_documents",
        "get_context",
    ]


def test_mygpt_bootstrap_refuses_an_existing_incompatible_dataset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bootstrap = load_bootstrap_module()
    dataset = {
        "name": "turing-way",
        "chat_model": "qwen2.5:3b",
        "embedding_model": "nomic-embed-text",
        "chunk_size": 1000,
        "chunking_method": "fixed_chunk_size",
        "use_overlap": True,
        "use_bm25": True,
        "documents_language": "english",
        "distance_function": "l2",
    }
    calls: list[str] = []

    def fake_request(url: str, payload: dict[str, object]) -> object:
        calls.append(url)
        if url.endswith("/api/get_datasets/"):
            return [{"dataset_name": "turing-way"}]
        if url.endswith("/api/get_dataset_details/"):
            return {
                "embedding_model": "different-model",
                "chunksize": 1000,
                "chunking_method": "fixed_chunk_size",
                "overlap": True,
                "use_bm25": True,
                "reranker": "None",
                "documents_language": "english",
                "distance_function": "l2",
                "dataset_size": 12,
            }
        if url.endswith("/api/get_documents/"):
            return {"documents": [{"paper_title": "wrong.md"}]}
        raise AssertionError(f"unexpected request: {url}")

    monkeypatch.setattr(bootstrap, "request_json", fake_request)

    with pytest.raises(bootstrap.IncompatibleDatasetError, match="refusing to upload"):
        bootstrap.existing_dataset_is_compatible(
            dataset, {"minimum_chunk_count": 1}, ["book/website/a.md"]
        )
    assert not any(call.endswith("/api/get_context/") for call in calls)
