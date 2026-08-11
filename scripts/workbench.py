"""Configure and validate the shareable development workbench."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import ssl
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from urllib.parse import urlsplit

import httpx

HEADER_NAME_PATTERN = re.compile(r"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$")
REQUIRED_ENVIRONMENT = (
    "AIMAAS_BASE_URL",
    "AIMAAS_MODEL_ID",
    "AIMAAS_API_KEY",
    "AIMAAS_API_KEY_HEADER",
)
PROVIDER_VALUE_ENVIRONMENT = ("AIMAAS_BASE_URL", "AIMAAS_MODEL_ID", "AIMAAS_API_KEY")
DEFAULT_OPENCODE_CONFIG = Path.home() / ".config/opencode/workbench-provider.json"
# Exact version required: OpenCode installs this package at runtime, and an
# unversioned reference would resolve to whatever is latest on the registry.
PROVIDER_SDK_PACKAGE = "@ai-sdk/openai-compatible@3.0.15"


class WorkbenchConfigurationError(ValueError):
    """Raised when required local workbench configuration is invalid."""


def provider_is_unconfigured(environment: Mapping[str, str]) -> bool:
    """True when no provider value is present, so the workbench stays offline-only.

    A partially completed configuration is not "unconfigured"; it must fail
    loudly instead of being silently skipped.
    """
    return all(not environment.get(name, "").strip() for name in PROVIDER_VALUE_ENVIRONMENT)


class FailureCategory(StrEnum):
    NETWORK = "network"
    CERTIFICATE_TRUST = "certificate-trust"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    RATE_LIMIT = "rate-limit"
    PROVIDER_SERVICE = "provider-service"


@dataclass(frozen=True)
class PreflightResult:
    ok: bool
    category: FailureCategory | None = None
    status_code: int | None = None


def _is_certificate_error(error: Exception) -> bool:
    current: BaseException | None = error
    while current is not None:
        if isinstance(current, ssl.SSLCertVerificationError):
            return True
        if "CERTIFICATE_VERIFY_FAILED" in str(current):
            return True
        current = current.__cause__ or current.__context__
    return False


@dataclass(frozen=True)
class ProviderSettings:
    base_url: str
    model_id: str
    api_key: str = field(repr=False)
    api_key_header: str = "api-key"

    @classmethod
    def from_environment(cls, environment: Mapping[str, str]) -> ProviderSettings:
        missing = [name for name in REQUIRED_ENVIRONMENT if not environment.get(name, "").strip()]
        if missing:
            raise WorkbenchConfigurationError(
                f"missing required workbench settings: {', '.join(missing)}"
            )

        base_url = environment["AIMAAS_BASE_URL"].strip().rstrip("/")
        parsed = urlsplit(base_url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise WorkbenchConfigurationError("AIMAAS_BASE_URL must be an HTTPS URL")
        if parsed.username or parsed.password:
            raise WorkbenchConfigurationError(
                "AIMAAS_BASE_URL must not contain embedded credentials"
            )
        if parsed.query or parsed.fragment:
            raise WorkbenchConfigurationError(
                "AIMAAS_BASE_URL must not contain a query string or fragment"
            )

        model_id = environment["AIMAAS_MODEL_ID"].strip()
        if any(ord(character) < 32 or ord(character) == 127 for character in model_id):
            raise WorkbenchConfigurationError("AIMAAS_MODEL_ID contains control characters")

        header_name = environment["AIMAAS_API_KEY_HEADER"].strip()
        if not HEADER_NAME_PATTERN.fullmatch(header_name):
            raise WorkbenchConfigurationError(
                "AIMAAS_API_KEY_HEADER must be a valid HTTP header name"
            )

        return cls(
            base_url=base_url,
            model_id=model_id,
            api_key=environment["AIMAAS_API_KEY"].strip(),
            api_key_header=header_name,
        )


async def run_model_preflight(
    settings: ProviderSettings,
    *,
    transport: httpx.AsyncBaseTransport | None = None,
) -> PreflightResult:
    url = f"{settings.base_url}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        settings.api_key_header: settings.api_key,
    }
    payload = {
        "model": settings.model_id,
        "messages": [
            {"role": "system", "content": "Reply with only the word ready."},
            {"role": "user", "content": "Connectivity check"},
        ],
        "max_completion_tokens": 8,
    }
    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(20.0),
            transport=transport,
        ) as client:
            response = await client.post(url, headers=headers, json=payload)
    except httpx.ConnectError as error:
        category = (
            FailureCategory.CERTIFICATE_TRUST
            if _is_certificate_error(error)
            else FailureCategory.NETWORK
        )
        return PreflightResult(ok=False, category=category)
    except (httpx.TimeoutException, httpx.NetworkError):
        return PreflightResult(ok=False, category=FailureCategory.NETWORK)

    categories = {
        401: FailureCategory.AUTHENTICATION,
        403: FailureCategory.AUTHORIZATION,
        429: FailureCategory.RATE_LIMIT,
    }
    if response.status_code in categories:
        return PreflightResult(
            ok=False,
            category=categories[response.status_code],
            status_code=response.status_code,
        )
    if response.status_code >= 400:
        return PreflightResult(
            ok=False,
            category=FailureCategory.PROVIDER_SERVICE,
            status_code=response.status_code,
        )
    try:
        choices = response.json()["choices"]
        if not choices:
            raise ValueError("empty choices")
    except (KeyError, TypeError, ValueError):
        return PreflightResult(
            ok=False,
            category=FailureCategory.PROVIDER_SERVICE,
            status_code=response.status_code,
        )
    return PreflightResult(ok=True, status_code=response.status_code)


def build_opencode_config(settings: ProviderSettings) -> dict[str, object]:
    model = {
        "name": "Approved Kimi model",
        "tool_call": True,
    }
    return {
        "$schema": "https://opencode.ai/config.json",
        "provider": {
            "aimaas": {
                "npm": PROVIDER_SDK_PACKAGE,
                "name": "Approved Kimi provider",
                "options": {
                    "baseURL": settings.base_url,
                    "headers": {
                        settings.api_key_header: "{env:AIMAAS_API_KEY}",
                    },
                    "timeout": 300000,
                    "chunkTimeout": 30000,
                },
                "models": {settings.model_id: model},
            }
        },
        "model": f"aimaas/{settings.model_id}",
        "small_model": f"aimaas/{settings.model_id}",
    }


def _write_config_file(config: dict[str, object], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(".tmp")
    content = json.dumps(config, indent=2) + "\n"
    temporary_path.write_text(content, encoding="utf-8")
    os.chmod(temporary_path, 0o600)
    temporary_path.replace(output_path)
    return output_path


def write_opencode_config(settings: ProviderSettings, output_path: Path) -> Path:
    return _write_config_file(build_opencode_config(settings), output_path)


def write_offline_opencode_config(output_path: Path) -> Path:
    return _write_config_file({"$schema": "https://opencode.ai/config.json"}, output_path)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    configure = subparsers.add_parser("configure-opencode")
    configure.add_argument(
        "--output",
        type=Path,
        default=Path(os.environ.get("OPENCODE_CONFIG", DEFAULT_OPENCODE_CONFIG)),
    )
    subparsers.add_parser("model-preflight")
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.command == "configure-opencode" and provider_is_unconfigured(os.environ):
        path = write_offline_opencode_config(args.output)
        print(f"SKIP provider configuration: offline mode, wrote {path}")
        print(
            "Complete config/workbench.env and reload it into your shell to enable the model route."
        )
        return 0
    try:
        settings = ProviderSettings.from_environment(os.environ)
    except WorkbenchConfigurationError as error:
        print(f"FAIL configuration: {error}")
        return 2

    if args.command == "configure-opencode":
        path = write_opencode_config(settings, args.output)
        print(f"PASS wrote OpenCode provider configuration: {path}")
        return 0
    if args.command == "model-preflight":
        result = asyncio.run(run_model_preflight(settings))
        if result.ok:
            print("PASS model connectivity: authenticated response received over verified TLS")
            return 0
        if result.category is None:
            print("FAIL model connectivity: internal error")
            return 2
        print(f"FAIL model connectivity: {result.category.value}")
        return {
            FailureCategory.NETWORK: 3,
            FailureCategory.CERTIFICATE_TRUST: 4,
            FailureCategory.AUTHENTICATION: 5,
            FailureCategory.AUTHORIZATION: 6,
            FailureCategory.RATE_LIMIT: 7,
            FailureCategory.PROVIDER_SERVICE: 8,
        }[result.category]
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
