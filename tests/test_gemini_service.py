import json
from types import SimpleNamespace

import pytest

from app.schemas.product import ProductInput
from app.services.gemini_mock import mock_genai_client_factory
from app.services.gemini_service import GeminiService


@pytest.mark.asyncio
async def test_transform_parses_valid_json(settings_test):
    factory = mock_genai_client_factory(response_text=json.dumps({"title": "T", "description": "D"}))

    svc = GeminiService(client_factory=factory, settings=settings_test)

    product = ProductInput(title="t", description="d")

    out = await svc.transform_product_description(product)

    assert out.title == "T"
    assert out.description == "D"


@pytest.mark.asyncio
async def test_transform_invalid_json_raises_valueerror(settings_test):
    factory = mock_genai_client_factory(response_text="not a json")
    svc = GeminiService(client_factory=factory, settings=settings_test)

    product = ProductInput(title="t", description="d")

    with pytest.raises(ValueError) as exc:
        await svc.transform_product_description(product)

    assert "Failed to parse Gemini response as JSON" in str(exc.value)


@pytest.mark.asyncio
async def test_transform_empty_text_raises(settings_test):
    # empty text and one candidate -> should raise ValueError('Empty response')
    factory = mock_genai_client_factory(response_text="", candidates=[SimpleNamespace(finish_reason="stop")])
    svc = GeminiService(client_factory=factory, settings=settings_test)

    product = ProductInput(title="t", description="d")

    with pytest.raises(ValueError) as exc:
        await svc.transform_product_description(product)

    assert "Empty response" in str(exc.value)


def test_manage_gemini_api_error_429(settings_test):
    svc = GeminiService(client_factory=mock_genai_client_factory(), settings=settings_test)

    with pytest.raises(ValueError) as exc:
        svc._manage_gemini_api_errors(SimpleNamespace(code=429, message="m"))

    assert "Rate limit exceeded" in str(exc.value)


def test_manage_gemini_api_error_503(settings_test):
    svc = GeminiService(client_factory=mock_genai_client_factory(), settings=settings_test)

    with pytest.raises(ValueError) as exc:
        svc._manage_gemini_api_errors(SimpleNamespace(code=503, message="service"))

    assert "service" in str(exc.value)
