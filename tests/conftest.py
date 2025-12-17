import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from app.config import Settings, get_settings
from app.main import app
from app.services.gemini_mock import mock_genai_client_factory
from app.services.gemini_service import GeminiService, get_gemini_service


@pytest.fixture(autouse=True)
def anyio_backend():
    return "asyncio"


@pytest.fixture
def settings_test(monkeypatch) -> Settings:
    """Configure environment variables for tests and return Settings.

    This uses `monkeypatch.setenv` so the real `get_settings()` reads
    environment variables. We clear the lru_cache on `get_settings` so a
    fresh Settings object is created for tests.
    """
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("GEMINI_API_KEY", "")
    monkeypatch.setenv("GEMINI_MODEL", "test-model")
    monkeypatch.setenv("GEMINI_TEMPERATURE", "0.0")
    monkeypatch.setenv("GEMINI_MAX_TOKENS", "256")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    monkeypatch.setenv("QUERY_TOKEN", "testq")
    monkeypatch.setenv("HEADER_TOKEN", "testh")

    # Clear cached settings so env changes take effect
    try:
        get_settings.cache_clear()
    except Exception:
        pass

    return get_settings()


@pytest.fixture
async def async_client(settings_test) -> AsyncGenerator[AsyncClient, None]:
    """Return an AsyncClient backed by the ASGI app. Fall back to a sync TestClient wrapped
    for async usage if ASGI transport is not available.
    """
    try:
        from httpx import ASGITransport

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    except Exception:
        # Fallback: wrap FastAPI TestClient for async tests
        from fastapi.testclient import TestClient

        class SyncClientAdapter:
            def __init__(self, sync_client: TestClient):
                self._client = sync_client

            async def get(self, url, **kwargs):
                return await asyncio.to_thread(lambda: self._client.get(url, **kwargs))

            async def post(self, url, **kwargs):
                return await asyncio.to_thread(lambda: self._client.post(url, **kwargs))

        sync_client = TestClient(app)
        adapter = SyncClientAdapter(sync_client)
        try:
            yield adapter
        finally:
            sync_client.close()


@pytest.fixture
def mock_genai_factory():
    """Provide a default mock genai client factory returning successful JSON."""
    return mock_genai_client_factory()


@pytest.fixture
def override_gemini_service(settings_test, mock_genai_factory):
    """Override the FastAPI dependency to use GeminiService with mock client.

    Ensures the override is removed after the test to keep tests independent.
    """
    # Register override: use mock GeminiService for tests only
    app.dependency_overrides[get_gemini_service] = lambda: GeminiService(
        client_factory=mock_genai_factory, settings=settings_test)

    yield

    # Cleanup
    app.dependency_overrides.pop(get_gemini_service, None)
