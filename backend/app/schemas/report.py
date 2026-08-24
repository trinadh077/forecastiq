from typing import Optional
from app.schemas.common import BaseSchema, TimestampSchema

class ReportBase(BaseSchema):
    title: str
    report_type: str

class ReportCreate(ReportBase):
    organization_id: str
    forecast_id: Optional[str] = None

class ReportRead(ReportBase, TimestampSchema):
    file_path: Optional[str] = None
    organization_id: str
    forecast_id: Optional[str] = None
