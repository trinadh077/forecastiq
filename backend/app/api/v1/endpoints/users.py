from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies.database import get_async_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserRead
from app.schemas.common import GenericResponse

router = APIRouter()

@router.get("", response_model=GenericResponse[List[UserRead]])
async def list_users(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    stmt = select(User)
    if current_user.organization_id:
        stmt = stmt.where(User.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    users = res.scalars().all()

    return GenericResponse(
        success=True,
        message="Users retrieved successfully",
        data=[UserRead.model_validate(u) for u in users]
    )
