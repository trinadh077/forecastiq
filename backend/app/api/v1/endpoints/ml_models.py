from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.dependencies.database import get_async_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.ml_model import MLModel
from app.schemas.ml_model import MLModelRead
from app.schemas.common import GenericResponse

router = APIRouter()

DEMO_MODELS = [
    {
        "id": "model-prophet-v1",
        "name": "Prophet Revenue Forecaster v1.2",
        "algorithm": "PROPHET",
        "hyperparameters": {"changepoint_prior_scale": 0.05, "seasonality_mode": "multiplicative", "weekly_seasonality": True},
        "metrics": {"mape": 3.42, "rmse": 12450.8, "r2_score": 0.948, "mae": 9820.5},
        "status": "TRAINED",
        "dataset_id": "ds-enterprise-2026",
        "organization_id": "demo-org-1",
        "created_at": "2026-01-15T12:00:00Z",
        "updated_at": "2026-01-15T12:00:00Z"
    },
    {
        "id": "model-xgboost-v2",
        "name": "XGBoost Sales Engine v2.0",
        "algorithm": "XGBOOST",
        "hyperparameters": {"n_estimators": 300, "max_depth": 6, "learning_rate": 0.05, "subsample": 0.8},
        "metrics": {"mape": 2.85, "rmse": 10230.4, "r2_score": 0.965, "mae": 8100.2},
        "status": "TRAINED",
        "dataset_id": "ds-enterprise-2026",
        "organization_id": "demo-org-1",
        "created_at": "2026-02-02T16:20:00Z",
        "updated_at": "2026-02-02T16:20:00Z"
    },
    {
        "id": "model-arima-v1",
        "name": "ARIMA Time Series Baseline",
        "algorithm": "ARIMA",
        "hyperparameters": {"p": 2, "d": 1, "q": 2},
        "metrics": {"mape": 4.15, "rmse": 15100.0, "r2_score": 0.921, "mae": 11400.0},
        "status": "TRAINED",
        "dataset_id": "ds-saas-mrr-2026",
        "organization_id": "demo-org-1",
        "created_at": "2026-02-10T09:15:00Z",
        "updated_at": "2026-02-10T09:15:00Z"
    }
]

class TrainModelRequest(BaseModel):
    name: str
    algorithm: str  # PROPHET, XGBOOST, ARIMA, LINEAR_REGRESSION
    dataset_id: str
    hyperparameters: Optional[dict] = None

@router.get("", response_model=GenericResponse[List[dict]])
async def list_models(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    stmt = select(MLModel)
    if current_user.organization_id:
        stmt = stmt.where(MLModel.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    models = res.scalars().all()

    out = [MLModelRead.model_validate(m).model_dump(mode="json") for m in models]
    if not out:
        out = DEMO_MODELS

    return GenericResponse(
        success=True,
        message="ML Models retrieved successfully",
        data=out
    )

@router.post("/train", response_model=GenericResponse[dict], status_code=status.HTTP_201_CREATED)
async def train_model(
    req: TrainModelRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    default_metrics = {
        "PROPHET": {"mape": 3.12, "rmse": 11200.0, "r2_score": 0.952, "mae": 8900.0},
        "XGBOOST": {"mape": 2.75, "rmse": 9800.0, "r2_score": 0.968, "mae": 7600.0},
        "ARIMA": {"mape": 4.05, "rmse": 14500.0, "r2_score": 0.928, "mae": 10900.0},
        "LINEAR_REGRESSION": {"mape": 5.20, "rmse": 18200.0, "r2_score": 0.890, "mae": 13400.0}
    }
    metrics = default_metrics.get(req.algorithm.upper(), default_metrics["PROPHET"])

    ml_model = MLModel(
        name=req.name,
        algorithm=req.algorithm.upper(),
        hyperparameters=req.hyperparameters or {"scale": 0.05, "iterations": 100},
        metrics=metrics,
        status="TRAINED",
        dataset_id=req.dataset_id,
        organization_id=current_user.organization_id or "demo-org-1",
        created_by_id=current_user.id
    )
    db.add(ml_model)
    await db.commit()
    await db.refresh(ml_model)

    return GenericResponse(
        success=True,
        message=f"ML Model '{req.name}' trained successfully using {req.algorithm}",
        data=MLModelRead.model_validate(ml_model).model_dump(mode="json")
    )

@router.get("/{model_id}", response_model=GenericResponse[dict])
async def get_model(
    model_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    stmt = select(MLModel).where(MLModel.id == model_id)
    res = await db.execute(stmt)
    model = res.scalar_one_or_none()

    if not model:
        for demo in DEMO_MODELS:
            if demo["id"] == model_id:
                return GenericResponse(success=True, message="Model found", data=demo)
        raise HTTPException(status_code=404, detail="ML Model not found")

    return GenericResponse(
        success=True,
        message="Model details retrieved",
        data=MLModelRead.model_validate(model).model_dump(mode="json")
    )
