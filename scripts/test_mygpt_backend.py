"""Live contract check for the MyGPT backend context endpoint."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

import httpx

DEFAULT_BASE_URL = "http://localhost:8000"
DEFAULT_TIMEOUT = 120.0
REQUEST_PAYLOAD = {
    "text": (
        "I have a GitHub repo with python scripts, and I am using all public data. How can I create reproducible environment using Turing Way best practices?"
    ),
    "model_type": "gpt-oss:20b",
    "dataset": "Turing_Way",
    "new_conversation": True,
    "previous_query": "",
    "no_context": False,
    "use_default_qrs": True,
    "question_best_distance": 0.2,
    "question_worst_distance": 1.7,
    "maximum_chunks_count": 5,
    "no_cutoff": False,
}

EXPECTED_TYPES = {
    "context": str,
    "relevance_score": (int, float),
    "semantic_score": (int, float),
    "keyword_score": (int, float),
    "rerank_score": (int, float),
    "sources": list,
}


def validate_response(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return [f"response must be a JSON object, got {type(data).__name__}"]

    errors = []
    for field, expected_type in EXPECTED_TYPES.items():
        if field not in data:
            errors.append(f"missing field: {field}")
        elif not isinstance(data[field], expected_type):
            expected_names = (
                "/".join(item.__name__ for item in expected_type)
                if isinstance(expected_type, tuple)
                else expected_type.__name__
            )
            errors.append(f"{field} must be {expected_names}, got {type(data[field]).__name__}")

    for field in ("relevance_score", "semantic_score", "keyword_score", "rerank_score"):
        value = data.get(field)
        if isinstance(value, (int, float)) and not 0 <= value <= 100:
            errors.append(f"{field} must be between 0 and 100, got {value}")

    return errors


def check_get_context(base_url: str, timeout: float) -> int:
    url = f"{base_url.rstrip('/')}/api/get_context/"
    try:
        response = httpx.post(url, json=REQUEST_PAYLOAD, timeout=timeout)
    except httpx.RequestError as error:
        print(f"FAIL: MyGPT backend is not reachable at {url}: {error}", file=sys.stderr)
        return 1

    if not response.is_success:
        content_type = response.headers.get("content-type", "unknown")
        print(
            f"FAIL: POST {url} returned HTTP {response.status_code} "
            f"with content type {content_type}",
            file=sys.stderr,
        )
        return 1

    try:
        data = response.json()
    except json.JSONDecodeError as error:
        print(f"FAIL: POST {url} did not return valid JSON: {error}", file=sys.stderr)
        return 1

    errors = validate_response(data)
    if errors:
        print("FAIL: response shape did not match the expected contract:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"PASS: POST {url} returned the expected response shape with {len(data['sources'])} sources"
    )
    if not data["sources"]:
        print("No source details returned.")
    for index, source in enumerate(data["sources"], start=1):
        print(f"\nSource {index}:")
        print(json.dumps(source, indent=2, ensure_ascii=False, default=str))
    return 0


def test_get_context_endpoint() -> None:
    base_url = os.environ.get("MYGPT_BASE_URL", DEFAULT_BASE_URL)
    timeout = float(os.environ.get("MYGPT_TIMEOUT", DEFAULT_TIMEOUT))

    assert check_get_context(base_url, timeout) == 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()
    return check_get_context(args.base_url, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())

""" 

Expected output:

PASS: POST http://localhost:8000/api/get_context/ returned the expected response shape with 3 sources

Source 1:
{
  "document": "the-turing-way",
  "page": 381,
  "start": "",
  "stop": "",
  "context": "Creating Project Repositories The Turing Way Community Wednesday 15th July, 2026 1 Prerequisites Prerequisite Importance Getting Started With GitHub Helpful 2 Summary This chapter introduces a step-by-step guide on how to set up a project repository. Specifically, we describe key documents that you should add to your repository in order to maintain documentation and ensure effective collaboration. We provide examples from GitHub repository hosted and maintainedby researchers in open science, however, the principles are applicable to any team-led online repository. 3 Motivation Online project repositories require documentation so that all collaborators are informed of the updates and contributors are provided with details they need to contribute eﬀiciently. Shared documents can help you get your ideas across to new or potential contributors. Contributions can be anything from new ideas to bug reports and actual code contributions. Open science practices described here will also make it",
  "vector_distance_raw": 198.061,
  "vector_score": 0.686,
  "rank": 1,
  "reranked_score": 0.691,
  "bm25_score_raw": 0,
  "bm25_score": 0,
  "bm25_rank": 0,
  "color_code": "green"
}

Source 2:
{
  "document": "the-turing-way",
  "page": 345,
  "context": "n Turing Institute have presented a method that achieves 97% accuracy on a large corpus of CSV files, with an improvement of 21% over existing approaches on non-standard CSV files. This research was made reproducible through the use of Make and is available through an online repository: https://github.com/alan-turing- institute/CSV_Wrangling. Below we will briefly describe what the Makefile for such a project looks like. For the complete file, please see the repository. The Makefile consists of several sections: 1. Data collection: because the data is collected from public sources, the repository contains a Python script that allows anyone to download the data through a simple make data command. 2. All the figures, tables, and constants used in the paper are generated based on the results from the experiments. To make it easy to recreate all results of a certain type, .PHONY targets are included that depend on all results of that type (so you could run make figures ). The rules for the",
  "bm25_score_raw": 7.9,
  "bm25_score": 0.39500001072883606,
  "vector_score": 0,
  "rank": 2,
  "reranked_score": 0.195,
  "vector_distance_raw": 0,
  "color_code": "yellow"
}

Source 3:
{
  "document": "the-turing-way",
  "page": 350,
  "context": ": data/%.csv scripts/generate_qqplot.py python scripts/generate_qqplot.py -i $< -o $@ output/report.pdf: report/report.tex $(FIGURES) cd report/ && pdflatex report.tex && mv report.pdf ../$@ clean: rm -f output/report.pdf rm -f $(HISTOGRAMS) $(QQPLOTS) You’ll notice that the rules for histograms and QQ-plots are very similar. As the number of scripts that you want to run on your data grows, this may lead to a large number of rules in the Makefile that are almost exactly the same. We can simplify this by creating a canned recipe that takes both the name of the script and the name of the genre as input: define run -script -on -data output/$(1)_$(2).png: data/$(2).csv scripts/generate_$(1).py python scripts/generate_$(1).py -i $$< -o $$@ endef Note that in this recipe we use $(1) for either histogram or qqplot and $(2) for the genre. These correspond to the expected function arguments to the run-script-on-data canned recipe. Also, notice that we use $$< and $$@ in the actual recipe, with",
  "bm25_score_raw": 7.48,
  "bm25_score": 0.37400001287460327,
  "vector_score": 0,
  "rank": 1,
  "reranked_score": 0.985,
  "vector_distance_raw": 0,
  "color_code": "yellow"
} """