from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.forecast import Forecast
from app.repositories.base import BaseRepository

class ForecastRepository(BaseRepository[Forecast]):
    def __init__(self, session: AsyncSession):
        super().__init__(Forecast, session)

    async def get_by_organization(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[Forecast]:
        query = select(Forecast).where(
            Forecast.organization_id == organization_id,
            Forecast.deleted_at.is_(None)
        ).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
