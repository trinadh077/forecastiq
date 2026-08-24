from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class IDSchema(BaseSchema):
    id: str

class TimestampSchema(IDSchema):
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

class GenericResponse(BaseSchema, Generic[T]):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[T] = None

class PaginatedResponse(BaseSchema, Generic[T]):
    total: int
    page: int
    size: int
    items: List[T]
