from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.report import Report
from app.repositories.base import BaseRepository

class ReportRepository(BaseRepository[Report]):
    def __init__(self, session: AsyncSession):
        super().__init__(Report, session)

    async def get_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Report]:
        query = select(Report).where(
            Report.organization_id == organization_id,
            Report.deleted_at.is_(None)
        ).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
