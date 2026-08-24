from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import pandas as pd
import numpy as np
import io
import json

from app.dependencies.database import get_async_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.ml_model import MLModel
from app.models.dataset import Dataset
from app.schemas.ml_model import MLModelRead
from app.schemas.common import GenericResponse
from app.config.logging import logger

router = APIRouter()


def _prepare_features(df: pd.DataFrame, target_col: str):
    """Prepare feature matrix and target vector from a DataFrame."""
    # Drop target and non-numeric columns
    feature_cols = []
    for col in df.columns:
        if col == target_col:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            feature_cols.append(col)

    if not feature_cols:
        raise ValueError("No numeric feature columns found in dataset")

    X = df[feature_cols].copy()
    y = df[target_col].copy()

    # Drop rows with NaN in target
    mask = y.notna()
    X = X[mask]
    y = y[mask]

    # Fill NaN in features with median
    X = X.fillna(X.median())

    return X, y, feature_cols


def _train_xgboost(X, y, params=None):
    """Train XGBoost model and return metrics."""
    from xgboost import XGBRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    default_params = {
        "n_estimators": 200,
        "max_depth": 6,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "random_state": 42,
        "verbosity": 0,
    }
    if params:
        default_params.update(params)

    model = XGBRegressor(**default_params)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mape = float(np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100)
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = float(r2_score(y_test, y_pred))
    mae = float(mean_absolute_error(y_test, y_pred))

    # Feature importance
    importances = dict(zip(X.columns.tolist(), [float(x) for x in model.feature_importances_]))

    return {
        "mape": round(mape, 2),
        "rmse": round(rmse, 2),
        "r2_score": round(r2, 4),
        "mae": round(mae, 2),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "feature_importance": importances,
    }


def _train_linear(X, y, params=None):
    """Train Ridge Regression and return metrics."""
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.preprocessing import StandardScaler

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    alpha = (params or {}).get("alpha", 1.0)
    model = Ridge(alpha=alpha, random_state=42)
    model.fit(X_train_s, y_train)

    y_pred = model.predict(X_test_s)

    mape = float(np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100)
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = float(r2_score(y_test, y_pred))
    mae = float(mean_absolute_error(y_test, y_pred))

    # Normalize coefficients to 0-1 range (percentages)
    raw_importances = [float(abs(x)) for x in model.coef_]
    total = sum(raw_importances)
    if total > 0:
        normalized = [v / total for v in raw_importances]
    else:
        normalized = [1.0 / len(raw_importances)] * len(raw_importances)
    importances = dict(zip(X.columns.tolist(), normalized))

    return {
        "mape": round(mape, 2),
        "rmse": round(rmse, 2),
        "r2_score": round(r2, 4),
        "mae": round(mae, 2),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "feature_importance": importances,
    }


def _train_random_forest(X, y, params=None):
    """Train Random Forest and return metrics."""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    default_params = {
        "n_estimators": 200,
        "max_depth": 10,
        "random_state": 42,
        "n_jobs": -1,
    }
    if params:
        default_params.update(params)

    model = RandomForestRegressor(**default_params)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mape = float(np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100)
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = float(r2_score(y_test, y_pred))
    mae = float(mean_absolute_error(y_test, y_pred))

    importances = dict(zip(X.columns.tolist(), [float(x) for x in model.feature_importances_]))

    return {
        "mape": round(mape, 2),
        "rmse": round(rmse, 2),
        "r2_score": round(r2, 4),
        "mae": round(mae, 2),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "feature_importance": importances,
    }


TRAINERS = {
    "XGBOOST": _train_xgboost,
    "LINEAR_REGRESSION": _train_linear,
    "RIDGE": _train_linear,
    "RANDOM_FOREST": _train_random_forest,
}


class TrainModelRequest(BaseModel):
    name: str
    algorithm: str
    dataset_id: str
    target_column: Optional[str] = None
    hyperparameters: Optional[dict] = None


@router.get("", response_model=GenericResponse[List[dict]])
async def list_models(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    stmt = select(MLModel).order_by(MLModel.created_at.desc())
    if current_user.organization_id:
        stmt = stmt.where(MLModel.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    models = res.scalars().all()
    out = [MLModelRead.model_validate(m).model_dump(mode="json") for m in models]
    return GenericResponse(success=True, message="ML Models retrieved successfully", data=out)


@router.post("/train", response_model=GenericResponse[dict], status_code=status.HTTP_201_CREATED)
async def train_model(
    req: TrainModelRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    # Load the dataset
    stmt = select(Dataset).where(Dataset.id == req.dataset_id)
    res = await db.execute(stmt)
    dataset = res.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Read the CSV file
    try:
        file_path = dataset.file_path
        # For uploaded files, try to read from the stored location
        # Since we store metadata but not actual files on Render, use the sample data
        schema = dataset.column_schema or {}
        sample_rows = schema.get("sample_rows", [])
        if sample_rows:
            df = pd.DataFrame(sample_rows)
        else:
            raise ValueError("No sample data available in dataset")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load dataset: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Dataset is empty")

    # Determine target column
    target_col = req.target_column
    if not target_col:
        # Auto-detect: find the first numeric column (usually revenue/target)
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if not numeric_cols:
            raise HTTPException(status_code=400, detail="No numeric columns found to use as target")
        target_col = numeric_cols[0]  # Default to first numeric column

    if target_col not in df.columns:
        raise HTTPException(status_code=400, detail=f"Target column '{target_col}' not found. Available: {list(df.columns)}")

    # Prepare features
    try:
        X, y, feature_cols = _prepare_features(df, target_col)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if len(X) < 10:
        raise HTTPException(status_code=400, detail=f"Not enough data rows ({len(X)}) for training. Need at least 10.")

    # Train the model
    algo = req.algorithm.upper()
    trainer = TRAINERS.get(algo)
    if not trainer:
        raise HTTPException(status_code=400, detail=f"Algorithm '{algo}' not supported. Use: {list(TRAINERS.keys())}")

    try:
        metrics = trainer(X, y, req.hyperparameters)
    except Exception as e:
        logger.error(f"Training error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

    # Save model to DB
    ml_model = MLModel(
        name=req.name,
        algorithm=algo,
        hyperparameters=req.hyperparameters or {},
        metrics=metrics,
        status="TRAINED",
        dataset_id=req.dataset_id,
        organization_id=current_user.organization_id or "demo-org-1",
        created_by_id=current_user.id,
    )
    db.add(ml_model)
    await db.commit()
    await db.refresh(ml_model)

    return GenericResponse(
        success=True,
        message=f"Model '{req.name}' trained successfully on {len(X)} rows using {algo}",
        data=MLModelRead.model_validate(ml_model).model_dump(mode="json"),
    )


@router.get("/{model_id}", response_model=GenericResponse[dict])
async def get_model(
    model_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    stmt = select(MLModel).where(MLModel.id == model_id)
    res = await db.execute(stmt)
    model = res.scalar_one_or_none()
    if not model:
        raise HTTPException(status_code=404, detail="ML Model not found")
    return GenericResponse(
        success=True,
        message="Model details retrieved",
        data=MLModelRead.model_validate(model).model_dump(mode="json"),
    )
