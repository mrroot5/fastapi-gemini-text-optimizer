import pytest


@pytest.mark.asyncio
async def test_health(async_client):
    r = await async_client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data


@pytest.mark.asyncio
async def test_transform_success(async_client, override_gemini_service, settings_test):
    payload = {
        "product": {
            "title": "Advanced Whey Protein Isolate Formula",
            "description": "Proprietary WPI blend with 25g protein per serving."
        }
    }

    headers = {"X-Token": settings_test.header_token}
    params = {"token": settings_test.query_token}

    r = await async_client.post("/products/transform", json=payload, headers=headers, params=params)
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert data["transformed"] is not None
    assert "title" in data["transformed"]


@pytest.mark.asyncio
async def test_transform_service_error(async_client, settings_test, monkeypatch):
    # Create a fake service that raises ValueError
    class FakeService:
        async def transform_product_description(self, product):
            raise ValueError("simulated failure")

    from app.main import app
    from app.services.gemini_service import get_gemini_service

    # Override dependency for this test only
    app.dependency_overrides[get_gemini_service] = lambda: FakeService()
    # Also bypass auth dependencies for this test
    from app.dependencies import get_query_token, get_token_header
    app.dependency_overrides[get_token_header] = lambda x_token=None: None
    app.dependency_overrides[get_query_token] = lambda token=None: None

    payload = {
        "product": {
            "title": "X",
            "description": "Y",
        }
    }

    headers = {"X-Token": settings_test.header_token}
    params = {"token": settings_test.query_token}

    r = await async_client.post("/products/transform", json=payload, headers=headers, params=params)
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is False
    assert data["error"] is not None

    # Cleanup override
    app.dependency_overrides.pop(get_gemini_service, None)
    app.dependency_overrides.pop(get_token_header, None)
    app.dependency_overrides.pop(get_query_token, None)
