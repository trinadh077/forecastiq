from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone
import math

from app.dependencies.database import get_async_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.forecast import Forecast
from app.schemas.forecast import ForecastRead
from app.schemas.common import GenericResponse

router = APIRouter()

class CreateForecastRequest(BaseModel):
    title: str
    horizon_days: int = Field(default=90, ge=7, le=365)
    confidence_interval: float = Field(default=0.95, ge=0.80, le=0.99)
    model_id: Optional[str] = "model-xgboost-v2"

def generate_forecast_chart_data(horizon_days: int, confidence: float) -> dict:
    today = datetime.now(timezone.utc)
    historical_points = []
    projected_points = []

    base_revenue = 185000.0
    growth_trend = 1.0018  # daily compounding growth ~5% monthly

    # Historical 60 days
    for i in range(60, 0, -1):
        dt = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        seasonal = 1.0 + 0.12 * math.sin(i / 7.0 * math.pi) + 0.05 * math.cos(i / 30.0 * math.pi)
        noise = (hash(dt) % 100 - 50) * 120.0
        val = round(base_revenue * (growth_trend ** (60 - i)) * seasonal + noise, 2)
        historical_points.append({"date": dt, "revenue": val, "type": "historical"})

    # Projected horizon_days
    last_val = historical_points[-1]["revenue"] if historical_points else base_revenue
    margin_multiplier = (1.0 - confidence) * 1.5 + 0.05

    total_projected_rev = 0.0
    for i in range(1, horizon_days + 1):
        dt = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        seasonal = 1.0 + 0.14 * math.sin((i + 60) / 7.0 * math.pi) + 0.08 * math.sin((i + 60) / 30.0 * math.pi)
        predicted = round(last_val * (growth_trend ** i) * seasonal, 2)
        
        uncertainty = predicted * margin_multiplier * math.sqrt(i / 30.0)
        lower_bound = round(max(0, predicted - uncertainty), 2)
        upper_bound = round(predicted + uncertainty, 2)

        total_projected_rev += predicted
        projected_points.append({
            "date": dt,
            "predicted": predicted,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "type": "projected"
        })

    arr_projection = round((total_projected_rev / horizon_days) * 365, 2)
    growth_rate = round(((projected_points[-1]["predicted"] - historical_points[0]["revenue"]) / historical_points[0]["revenue"]) * 100, 2)

    return {
        "summary": {
            "total_projected_revenue": round(total_projected_rev, 2),
            "projected_arr": arr_projection,
            "growth_rate_pct": growth_rate,
            "horizon_days": horizon_days,
            "confidence_interval": confidence,
            "avg_daily_revenue": round(total_projected_rev / horizon_days, 2)
        },
        "historical": historical_points,
        "projected": projected_points
    }

DEMO_FORECASTS = [
    {
        "id": "forecast-q2-2026",
        "title": "Q2-Q4 2026 Sales Revenue Projection",
        "horizon_days": 90,
        "confidence_interval": 0.95,
        "forecast_data": generate_forecast_chart_data(90, 0.95),
        "organization_id": "demo-org-1",
        "model_id": "model-xgboost-v2",
        "created_by_id": "demo-user-1",
        "created_at": "2026-02-15T10:00:00Z",
        "updated_at": "2026-02-15T10:00:00Z"
    }
]

@router.get("", response_model=GenericResponse[List[dict]])
async def list_forecasts(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    stmt = select(Forecast)
    if current_user.organization_id:
        stmt = stmt.where(Forecast.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    forecasts = res.scalars().all()

    out = [ForecastRead.model_validate(f).model_dump(mode="json") for f in forecasts]
    if not out:
        out = DEMO_FORECASTS

    return GenericResponse(
        success=True,
        message="Forecasts retrieved successfully",
        data=out
    )

@router.post("", response_model=GenericResponse[dict], status_code=status.HTTP_201_CREATED)
async def create_forecast(
    req: CreateForecastRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    forecast_data = generate_forecast_chart_data(req.horizon_days, req.confidence_interval)

    forecast = Forecast(
        title=req.title,
        horizon_days=req.horizon_days,
        confidence_interval=req.confidence_interval,
        forecast_data=forecast_data,
        organization_id=current_user.organization_id or "demo-org-1",
        model_id=req.model_id or "model-xgboost-v2",
        created_by_id=current_user.id
    )
    db.add(forecast)
    await db.commit()
    await db.refresh(forecast)

    return GenericResponse(
        success=True,
        message=f"Forecast '{req.title}' generated successfully",
        data=ForecastRead.model_validate(forecast).model_dump(mode="json")
    )

@router.get("/{forecast_id}", response_model=GenericResponse[dict])
async def get_forecast(
    forecast_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    stmt = select(Forecast).where(Forecast.id == forecast_id)
    res = await db.execute(stmt)
    forecast = res.scalar_one_or_none()

    if not forecast:
        for demo in DEMO_FORECASTS:
            if demo["id"] == forecast_id:
                return GenericResponse(success=True, message="Forecast found", data=demo)
        raise HTTPException(status_code=404, detail="Forecast not found")

    return GenericResponse(
        success=True,
        message="Forecast details retrieved",
        data=ForecastRead.model_validate(forecast).model_dump(mode="json")
    )
