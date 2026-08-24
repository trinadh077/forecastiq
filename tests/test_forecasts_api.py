import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_datasets_and_forecasts_flow(async_client: AsyncClient):
    # Register & get auth token
    reg_payload = {
        "email": "analyst@forecastiq.ai",
        "password": "Password123!",
        "full_name": "Sales Analyst",
        "organization_name": "Revenue Corp"
    }
    reg_res = await async_client.post("/api/v1/auth/register", json=reg_payload)
    token = reg_res.json()["data"]["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # List datasets
    ds_res = await async_client.get("/api/v1/datasets", headers=headers)
    assert ds_res.status_code == 200
    assert len(ds_res.json()["data"]) > 0

    # Create Forecast
    fc_payload = {
        "title": "Q3 Revenue Forecast",
        "horizon_days": 90,
        "confidence_interval": 0.95,
        "model_id": "model-xgboost-v2"
    }
    fc_res = await async_client.post("/api/v1/forecasts", json=fc_payload, headers=headers)
    assert fc_res.status_code == 201
    fc_data = fc_res.json()["data"]
    assert fc_data["title"] == "Q3 Revenue Forecast"
    assert "projected" in fc_data["forecast_data"]
    assert len(fc_data["forecast_data"]["projected"]) == 90
