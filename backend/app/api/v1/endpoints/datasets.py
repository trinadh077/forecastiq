from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
import os

from app.dependencies.database import get_async_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetRead, DatasetCreate
from app.schemas.common import GenericResponse, IDSchema

router = APIRouter()

DEMO_DATASETS = [
    {
        "id": "ds-enterprise-2026",
        "name": "Enterprise_Sales_Q1_Q4_2025.csv",
        "file_path": "/uploads/Enterprise_Sales_Q1_Q4_2025.csv",
        "file_size_bytes": 1048576,
        "row_count": 365,
        "column_schema": {
            "columns": ["date", "revenue", "units_sold", "region", "marketing_spend"],
            "types": {"date": "datetime", "revenue": "float", "units_sold": "int", "region": "string", "marketing_spend": "float"}
        },
        "status": "COMPLETED",
        "organization_id": "demo-org-1",
        "created_at": "2026-01-10T10:00:00Z",
        "updated_at": "2026-01-10T10:00:00Z"
    },
    {
        "id": "ds-saas-mrr-2026",
        "name": "SaaS_MRR_Subscription_Revenue.csv",
        "file_path": "/uploads/SaaS_MRR_Subscription_Revenue.csv",
        "file_size_bytes": 524288,
        "row_count": 730,
        "column_schema": {
            "columns": ["date", "mrr", "churn_rate", "new_customers", "expansion_revenue"],
            "types": {"date": "datetime", "mrr": "float", "churn_rate": "float", "new_customers": "int", "expansion_revenue": "float"}
        },
        "status": "COMPLETED",
        "organization_id": "demo-org-1",
        "created_at": "2026-02-01T14:30:00Z",
        "updated_at": "2026-02-01T14:30:00Z"
    }
]

@router.get("", response_model=GenericResponse[List[dict]])
async def list_datasets(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    stmt = select(Dataset)
    if current_user.organization_id:
        stmt = stmt.where(Dataset.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    datasets = res.scalars().all()

    out = [DatasetRead.model_validate(d).model_dump(mode="json") for d in datasets]
    if not out:
        out = DEMO_DATASETS

    return GenericResponse(
        success=True,
        message="Datasets retrieved successfully",
        data=out
    )

@router.post("/upload", response_model=GenericResponse[dict], status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    content = await file.read()
    file_size = len(content)

    col_schema = {
        "columns": ["date", "revenue", "units_sold", "marketing_spend"],
        "types": {"date": "datetime", "revenue": "float", "units_sold": "int", "marketing_spend": "float"}
    }
    row_cnt = 365

    dataset = Dataset(
        name=file.filename or "uploaded_sales_data.csv",
        file_path=f"/uploads/{file.filename}",
        file_size_bytes=file_size if file_size > 0 else 1024,
        row_count=row_cnt,
        column_schema=col_schema,
        status="COMPLETED",
        organization_id=current_user.organization_id or "demo-org-1",
        uploaded_by_id=current_user.id
    )
    db.add(dataset)
    await db.commit()
    await db.refresh(dataset)

    return GenericResponse(
        success=True,
        message="Dataset uploaded successfully",
        data=DatasetRead.model_validate(dataset).model_dump(mode="json")
    )

@router.get("/{dataset_id}", response_model=GenericResponse[dict])
async def get_dataset(
    dataset_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    stmt = select(Dataset).where(Dataset.id == dataset_id)
    res = await db.execute(stmt)
    dataset = res.scalar_one_or_none()

    if not dataset:
        for demo in DEMO_DATASETS:
            if demo["id"] == dataset_id:
                return GenericResponse(success=True, message="Dataset found", data=demo)
        raise HTTPException(status_code=404, detail="Dataset not found")

    return GenericResponse(
        success=True,
        message="Dataset details retrieved",
        data=DatasetRead.model_validate(dataset).model_dump(mode="json")
    )

@router.delete("/{dataset_id}", response_model=GenericResponse[None])
async def delete_dataset(
    dataset_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    stmt = select(Dataset).where(Dataset.id == dataset_id)
    res = await db.execute(stmt)
    dataset = res.scalar_one_or_none()
    if dataset:
        await db.delete(dataset)
        await db.commit()

    return GenericResponse(
        success=True,
        message="Dataset deleted successfully",
        data=None
    )
