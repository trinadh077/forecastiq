from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Organization
from app.repositories.base import BaseRepository

class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, session: AsyncSession):
        super().__init__(Organization, session)

    async def get_by_slug(self, slug: str) -> Optional[Organization]:
        query = select(Organization).where(Organization.slug == slug.lower(), Organization.deleted_at.is_(None))
        result = await self.session.execute(query)
        return result.scalars().first()
