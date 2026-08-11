import json
from pathlib import Path

import httpx
import pytest

from scripts.workbench import (
    FailureCategory,
    ProviderSettings,
    WorkbenchConfigurationError,
    build_opencode_config,
    provider_is_unconfigured,
    run_model_preflight,
    write_offline_opencode_config,
    write_opencode_config,
)

VALID_ENVIRONMENT = {
    "AIMAAS_BASE_URL": "https://provider.example/openai/v1",
    "AIMAAS_MODEL_ID": "approved-model",
    "AIMAAS_API_KEY": "test-secret-value",
    "AIMAAS_API_KEY_HEADER": "api-key",
}


def test_unconfigured_provider_is_detected_only_when_every_value_is_blank() -> None:
    assert provider_is_unconfigured({}) is True
    assert provider_is_unconfigured({"AIMAAS_API_KEY_HEADER": "api-key"}) is True
    assert provider_is_unconfigured({"AIMAAS_BASE_URL": "", "AIMAAS_API_KEY": "  "}) is True
    assert provider_is_unconfigured(VALID_ENVIRONMENT) is False
    assert provider_is_unconfigured({"AIMAAS_BASE_URL": "https://provider.example"}) is False


def test_offline_opencode_stub_contains_no_provider(tmp_path: Path) -> None:
    output_path = tmp_path / "workbench-provider.json"

    result = write_offline_opencode_config(output_path)

    assert result == output_path
    assert json.loads(output_path.read_text(encoding="utf-8")) == {
        "$schema": "https://opencode.ai/config.json"
    }
    assert not output_path.with_suffix(".tmp").exists()


def test_provider_settings_require_all_values() -> None:
    with pytest.raises(WorkbenchConfigurationError, match="AIMAAS_API_KEY"):
        ProviderSettings.from_environment({**VALID_ENVIRONMENT, "AIMAAS_API_KEY": ""})


def test_provider_settings_require_https_without_credentials() -> None:
    with pytest.raises(WorkbenchConfigurationError, match="HTTPS"):
        ProviderSettings.from_environment(
            {**VALID_ENVIRONMENT, "AIMAAS_BASE_URL": "http://provider.example/v1"}
        )
    with pytest.raises(WorkbenchConfigurationError, match="credentials"):
        ProviderSettings.from_environment(
            {
                **VALID_ENVIRONMENT,
                "AIMAAS_BASE_URL": "https://user:password@provider.example/v1",
            }
        )


def test_provider_settings_hide_the_api_key_from_repr() -> None:
    settings = ProviderSettings.from_environment(VALID_ENVIRONMENT)
    assert VALID_ENVIRONMENT["AIMAAS_API_KEY"] not in repr(settings)


def test_opencode_config_uses_environment_reference_for_secret() -> None:
    settings = ProviderSettings.from_environment(VALID_ENVIRONMENT)
    config = build_opencode_config(settings)
    serialized = json.dumps(config)
    provider = config["provider"]["aimaas"]

    assert VALID_ENVIRONMENT["AIMAAS_API_KEY"] not in serialized
    assert provider["npm"] == "@ai-sdk/openai-compatible@3.0.15"
    assert provider["options"]["baseURL"] == VALID_ENVIRONMENT["AIMAAS_BASE_URL"]
    assert provider["options"]["headers"] == {"api-key": "{env:AIMAAS_API_KEY}"}
    assert config["model"] == "aimaas/approved-model"


def test_write_opencode_config_is_atomic_and_secret_free(tmp_path: Path) -> None:
    settings = ProviderSettings.from_environment(VALID_ENVIRONMENT)
    output_path = tmp_path / "workbench-provider.json"

    result = write_opencode_config(settings, output_path)

    assert result == output_path
    assert output_path.is_file()
    assert VALID_ENVIRONMENT["AIMAAS_API_KEY"] not in output_path.read_text(encoding="utf-8")
    assert not output_path.with_suffix(".tmp").exists()


@pytest.mark.asyncio
async def test_model_preflight_sends_required_header_without_logging_secret() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["api-key"] == VALID_ENVIRONMENT["AIMAAS_API_KEY"]
        assert request.url.path.endswith("/chat/completions")
        payload = json.loads(request.content)
        assert payload["model"] == VALID_ENVIRONMENT["AIMAAS_MODEL_ID"]
        return httpx.Response(
            200,
            json={"choices": [{"message": {"role": "assistant", "content": "ok"}}]},
        )

    settings = ProviderSettings.from_environment(VALID_ENVIRONMENT)
    result = await run_model_preflight(settings, transport=httpx.MockTransport(handler))

    assert result.ok is True
    assert result.category is None
    assert VALID_ENVIRONMENT["AIMAAS_API_KEY"] not in repr(result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status_code", "category"),
    [
        (401, FailureCategory.AUTHENTICATION),
        (403, FailureCategory.AUTHORIZATION),
        (429, FailureCategory.RATE_LIMIT),
        (500, FailureCategory.PROVIDER_SERVICE),
    ],
)
async def test_model_preflight_classifies_http_failures(
    status_code: int,
    category: FailureCategory,
) -> None:
    transport = httpx.MockTransport(lambda _request: httpx.Response(status_code))
    result = await run_model_preflight(
        ProviderSettings.from_environment(VALID_ENVIRONMENT),
        transport=transport,
    )

    assert result.ok is False
    assert result.category is category
    assert result.status_code == status_code


@pytest.mark.asyncio
async def test_model_preflight_rejects_invalid_success_payload() -> None:
    transport = httpx.MockTransport(lambda _request: httpx.Response(200, json={}))
    result = await run_model_preflight(
        ProviderSettings.from_environment(VALID_ENVIRONMENT),
        transport=transport,
    )

    assert result.category is FailureCategory.PROVIDER_SERVICE
