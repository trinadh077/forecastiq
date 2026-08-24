from typing import Optional, Dict, Any
from app.schemas.common import BaseSchema, TimestampSchema

class DatasetBase(BaseSchema):
    name: str

class DatasetCreate(DatasetBase):
    organization_id: str
    file_path: str
    file_size_bytes: int

class DatasetRead(DatasetBase, TimestampSchema):
    file_path: str
    file_size_bytes: int
    row_count: Optional[int] = None
    column_schema: Optional[Dict[str, Any]] = None
    status: str
    organization_id: str
    uploaded_by_id: Optional[str] = None
