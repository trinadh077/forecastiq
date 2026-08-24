from typing import Optional, Dict, Any
from app.schemas.common import BaseSchema, TimestampSchema

class ForecastBase(BaseSchema):
    title: str
    horizon_days: int = 30
    confidence_interval: float = 0.95

class ForecastCreate(ForecastBase):
    organization_id: str
    model_id: str

class ForecastRead(ForecastBase, TimestampSchema):
    forecast_data: Optional[Dict[str, Any]] = None
    organization_id: str
    model_id: str
    created_by_id: Optional[str] = None
