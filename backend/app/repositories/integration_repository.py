from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.integration import Integration
from app.repositories.base import BaseRepository

class IntegrationRepository(BaseRepository[Integration]):
    def __init__(self, session: AsyncSession):
        super().__init__(Integration, session)

    async def get_by_provider(self, organization_id: str, provider: str) -> Optional[Integration]:
        query = select(Integration).where(
            Integration.organization_id == organization_id,
            Integration.provider == provider,
            Integration.deleted_at.is_(None)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
