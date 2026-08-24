from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dataset import Dataset
from app.repositories.base import BaseRepository

class DatasetRepository(BaseRepository[Dataset]):
    def __init__(self, session: AsyncSession):
        super().__init__(Dataset, session)

    async def get_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Dataset]:
        query = select(Dataset).where(
            Dataset.organization_id == organization_id,
            Dataset.deleted_at.is_(None)
        ).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
