from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ml_model import MLModel
from app.repositories.base import BaseRepository

class MLModelRepository(BaseRepository[MLModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(MLModel, session)

    async def get_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[MLModel]:
        query = select(MLModel).where(
            MLModel.organization_id == organization_id,
            MLModel.deleted_at.is_(None)
        ).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
