from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from datetime import datetime, timezone
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import BaseModel
from app.core.exceptions import ForecastIQException

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id_str: str) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id_str, self.model.deleted_at.is_(None))
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_multi(
        self,
        filters: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        query = select(self.model).where(self.model.deleted_at.is_(None))
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.where(getattr(self.model, key) == value)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        query = select(func.count(self.model.id)).where(self.model.deleted_at.is_(None))
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.where(getattr(self.model, key) == value)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def create(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: ModelType, update_data: Dict[str, Any]) -> ModelType:
        # Check optimistic locking version
        current_version = instance.version
        update_data["version"] = current_version + 1
        update_data["updated_at"] = datetime.now(timezone.utc)
        
        for key, value in update_data.items():
            if hasattr(instance, key) and value is not None:
                setattr(instance, key, value)

        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def soft_delete(self, instance: ModelType) -> None:
        instance.deleted_at = datetime.now(timezone.utc)
        self.session.add(instance)
        await self.session.flush()
