from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.role import Role
from app.repositories.base import BaseRepository

class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(Role, session)

    async def get_by_name(self, name: str) -> Optional[Role]:
        query = select(Role).where(Role.name == name.upper(), Role.deleted_at.is_(None))
        result = await self.session.execute(query)
        return result.scalars().first()
