from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies.database import get_async_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.report import Report
from app.schemas.report import ReportRead
from app.schemas.common import GenericResponse

router = APIRouter()

DEMO_REPORTS = [
    {
        "id": "report-executive-q1-2026",
        "title": "Executive Sales & Revenue Intelligence Summary Q1 2026",
        "report_type": "EXECUTIVE_SUMMARY",
        "file_path": "/reports/Executive_Sales_Summary_Q1_2026.pdf",
        "forecast_id": "forecast-q2-2026",
        "organization_id": "demo-org-1",
        "generated_by_id": "demo-user-1",
        "created_at": "2026-02-16T11:00:00Z",
        "updated_at": "2026-02-16T11:00:00Z"
    }
]

@router.get("", response_model=GenericResponse[List[dict]])
async def list_reports(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    stmt = select(Report)
    if current_user.organization_id:
        stmt = stmt.where(Report.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    reports = res.scalars().all()

    out = [ReportRead.model_validate(r).model_dump(mode="json") for r in reports]
    if not out:
        out = DEMO_REPORTS

    return GenericResponse(
        success=True,
        message="Reports retrieved successfully",
        data=out
    )
