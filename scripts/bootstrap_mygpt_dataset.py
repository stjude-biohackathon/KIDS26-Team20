"""Import the pinned Turing Way corpus into the local MyGPT service."""

from __future__ import annotations

import io
import json
import os
from collections.abc import Mapping, Sequence
from pathlib import Path
from urllib.request import urlopen

import yaml

ROOT = Path("/workspace")
MYGPT_URL = os.environ.get("MYGPT_URL", "http://mygpt-backend:8000")


class IncompatibleDatasetError(RuntimeError):
    """Raised when an existing dataset cannot be safely reused."""


def request_json(url: str, payload: dict[str, object]) -> object:
    import requests

    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()


def source_paths(source: Mapping[str, str]) -> list[str]:
    tree_url = f"https://api.github.com/repos/{source['repository']}/git/trees/{source['ref']}"
    with urlopen(f"{tree_url}?recursive=1", timeout=60) as response:  # nosec B310: pinned GitHub source
        tree = json.load(response)["tree"]
    prefix = f"{source['content_root']}/"
    paths = [
        entry["path"]
        for entry in tree
        if entry.get("type") == "blob"
        and entry["path"].startswith(prefix)
        and entry["path"].lower().endswith(".md")
    ]
    if not paths:
        raise RuntimeError("The pinned Turing Way source contains no Markdown pages.")
    return sorted(paths)


def validate_provenance(
    provenance: Mapping[str, object], source: Mapping[str, str], paths: Sequence[str]
) -> None:
    source_provenance = provenance.get("source")
    if not isinstance(source_provenance, Mapping):
        raise RuntimeError("Bootstrap provenance must define its source.")
    for key in ("repository", "ref", "content_root"):
        if source_provenance.get(key) != source[key]:
            raise RuntimeError(
                f"Bootstrap provenance {key} does not match {source[key]!r} in corpus/sources.yaml."
            )
    if provenance.get("expected_document_count") != len(paths):
        raise RuntimeError(
            "Pinned source document count differs from mygpt-bootstrap.yaml; "
            "review and update the tracked provenance before importing."
        )
    if not isinstance(provenance.get("minimum_chunk_count"), int) or (
        provenance["minimum_chunk_count"] < 1
    ):
        raise RuntimeError("Bootstrap provenance must require at least one indexed chunk.")


def register_models(dataset: Mapping[str, object]) -> None:
    request_json(
        f"{MYGPT_URL}/api/add_ollama_models/",
        {"llms": [{"name": dataset["chat_model"], "size": 0}]},
    )
    request_json(
        f"{MYGPT_URL}/api/add_embedding_models/",
        {
            "embedding_models": [
                {
                    "name": dataset["embedding_model"],
                    "size": 0,
                    "source": dataset["embedding_source"],
                }
            ]
        },
    )


def bootstrap_identity() -> dict[str, str]:
    return {
        # MyGPT's local library APIs identify unauthenticated datasets with
        # these sentinel values. Using the same identity for reads and writes
        # makes repeat bootstrap checks see the dataset they created.
        "user": "-",
        "user_email": "-",
        "user_group": "-",
    }


def live_retrieval_is_ready(dataset: Mapping[str, object]) -> bool:
    response = request_json(
        f"{MYGPT_URL}/api/get_context/",
        {
            "text": "What is The Turing Way and how does it support reproducible research?",
            "model_type": dataset["chat_model"],
            "dataset": dataset["name"],
            "new_conversation": True,
            "previous_query": "",
            "no_context": False,
            "use_default_qrs": True,
            "question_best_distance": 0.2,
            "question_worst_distance": 1.7,
            "maximum_chunks_count": 5,
            "no_cutoff": False,
            "skip_highlight": True,
        },
    )
    return (
        isinstance(response, Mapping)
        and isinstance(response.get("sources"), list)
        and bool(response["sources"])
    )


def existing_dataset_is_compatible(
    dataset: Mapping[str, object], provenance: Mapping[str, object], paths: Sequence[str]
) -> bool:
    """Return whether MyGPT proves the named dataset is this live corpus.

    MyGPT has no provenance field. Its documented dataset, document, and
    retrieval endpoints therefore jointly provide the strongest safe check
    without altering an existing dataset.
    """
    identity = bootstrap_identity()
    datasets = request_json(
        f"{MYGPT_URL}/api/get_datasets/",
        {"user_email": identity["user_email"], "user_group": identity["user_group"]},
    )
    if not isinstance(datasets, list):
        raise IncompatibleDatasetError("MyGPT returned an invalid dataset list.")
    matches = [
        item
        for item in datasets
        if isinstance(item, Mapping) and item.get("dataset_name") == dataset["name"]
    ]
    if not matches:
        return False
    if len(matches) != 1:
        raise IncompatibleDatasetError(
            f"MyGPT returned multiple {dataset['name']!r} datasets; refusing to upload."
        )

    details = request_json(
        f"{MYGPT_URL}/api/get_dataset_details/",
        {
            "dataset": dataset["name"],
            "user_email": identity["user_email"],
            "user_group": identity["user_group"],
        },
    )
    documents_response = request_json(
        f"{MYGPT_URL}/api/get_documents/",
        {
            "dataset": dataset["name"],
            "user_email": identity["user_email"],
            "user_group": identity["user_group"],
        },
    )
    if not isinstance(details, Mapping) or not isinstance(documents_response, Mapping):
        raise IncompatibleDatasetError("MyGPT returned invalid dataset compatibility data.")

    expected_settings = {
        "embedding_model": dataset["embedding_model"],
        "chunksize": dataset["chunk_size"],
        "chunking_method": dataset["chunking_method"],
        "overlap": dataset["use_overlap"],
        "use_bm25": dataset["use_bm25"],
        "reranker": "None",
        "documents_language": dataset["documents_language"],
        "distance_function": dataset["distance_function"],
    }
    mismatches = [
        key for key, expected in expected_settings.items() if details.get(key) != expected
    ]
    dataset_size = details.get("dataset_size")
    if not isinstance(dataset_size, int) or dataset_size < provenance["minimum_chunk_count"]:
        mismatches.append("dataset_size")

    documents = documents_response.get("documents")
    titles = (
        [document.get("paper_title") for document in documents if isinstance(document, Mapping)]
        if isinstance(documents, list)
        else []
    )
    expected_titles = list(paths)
    if (
        len(titles) != len(expected_titles)
        or len(set(titles)) != len(titles)
        or set(titles) != set(expected_titles)
    ):
        mismatches.append("documents")

    if mismatches:
        raise IncompatibleDatasetError(
            "Existing dataset is not the tracked Turing Way corpus "
            f"({', '.join(mismatches)} differs); refusing to upload or overwrite it."
        )
    if not live_retrieval_is_ready(dataset):
        raise IncompatibleDatasetError(
            "Existing dataset has no live Turing Way retrieval sources; refusing to upload."
        )
    return True


def build_pdf_files(
    source: Mapping[str, str], paths: Sequence[str]
) -> list[tuple[str, tuple[str, io.BytesIO, str]]]:
    import pymupdf

    files: list[tuple[str, tuple[str, io.BytesIO, str]]] = []
    for path in paths:
        raw_url = f"https://raw.githubusercontent.com/{source['repository']}/{source['ref']}/{path}"
        with urlopen(raw_url, timeout=60) as response:  # nosec B310: pinned GitHub source
            markdown = response.read().decode("utf-8")
        document = pymupdf.open()
        for start in range(0, len(markdown), 3500):
            page = document.new_page()
            page.insert_textbox(
                pymupdf.Rect(36, 36, page.rect.width - 36, page.rect.height - 36),
                markdown[start : start + 3500],
                fontsize=8,
            )
        content = io.BytesIO(document.tobytes())
        document.close()
        files.append(("paper_attachment", (f"{Path(path).stem}.pdf", content, "application/pdf")))
    return files


def main() -> int:
    config = yaml.safe_load((ROOT / "config/mygpt-bootstrap.yaml").read_text(encoding="utf-8"))
    dataset = config["dataset"]
    provenance = config["provenance"]
    source = yaml.safe_load((ROOT / dataset["source_manifest"]).read_text(encoding="utf-8"))[
        "sources"
    ][0]
    paths = source_paths(source)
    validate_provenance(provenance, source, paths)

    register_models(dataset)
    if existing_dataset_is_compatible(dataset, provenance, paths):
        print(f"MyGPT dataset {dataset['name']!r} is compatible and live; skipping upload.")
        return 0

    files = build_pdf_files(source, paths)

    form = {
        "dataset_name": dataset["name"],
        "paper_title": paths,
        **bootstrap_identity(),
        "use_overlap": "Yes" if dataset["use_overlap"] else "No",
        "chunking_method": dataset["chunking_method"],
        "chunk_size": str(dataset["chunk_size"]),
        "distance_function": dataset["distance_function"],
        "use_bm25": "Yes" if dataset["use_bm25"] else "No",
        "reranker": "None",
        "documents_language": dataset["documents_language"],
        "embedding_model": dataset["embedding_model"],
    }
    import requests

    try:
        response = requests.post(
            f"{MYGPT_URL}/api/upload_documents/",
            data=form,
            files=files,
            timeout=1800,
        )
        response.raise_for_status()
        try:
            upload_response = response.json()
        except ValueError as error:
            raise RuntimeError("MyGPT returned invalid JSON after uploading the corpus.") from error
    finally:
        for _, (_, content, _) in files:
            content.close()
    if not isinstance(upload_response, Mapping) or upload_response.get("uploaded") is not True:
        raise RuntimeError(f"MyGPT did not confirm the upload: {upload_response!r}")
    try:
        existing_dataset_is_compatible(dataset, provenance, paths)
    except IncompatibleDatasetError as error:
        raise RuntimeError(
            "MyGPT upload completed but the required post-upload compatibility check failed; "
            "do not retry automatically because the dataset may be partially imported."
        ) from error
    print(f"MyGPT dataset {dataset['name']!r} was imported and passed the live readiness check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
