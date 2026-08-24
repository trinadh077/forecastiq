from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subscription import Subscription
from app.repositories.base import BaseRepository

class SubscriptionRepository(BaseRepository[Subscription]):
    def __init__(self, session: AsyncSession):
        super().__init__(Subscription, session)

    async def get_by_organization(self, organization_id: str) -> Optional[Subscription]:
        query = select(Subscription).where(
            Subscription.organization_id == organization_id,
            Subscription.deleted_at.is_(None)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
