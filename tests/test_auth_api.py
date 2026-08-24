import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_and_login_flow(async_client: AsyncClient):
    # Register user
    reg_payload = {
        "email": "testuser@forecastiq.ai",
        "password": "Password123!",
        "full_name": "Test Analyst",
        "organization_name": "Acme Forecasting Inc"
    }
    reg_res = await async_client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    data = reg_res.json()
    assert data["success"] is True
    assert "access_token" in data["data"]["token"]

    # Login user
    login_payload = {
        "email": "testuser@forecastiq.ai",
        "password": "Password123!"
    }
    login_res = await async_client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token = login_res.json()["data"]["token"]["access_token"]

    # Get Me
    me_res = await async_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_res.status_code == 200
    assert me_res.json()["data"]["email"] == "testuser@forecastiq.ai"
