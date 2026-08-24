from typing import Optional, Dict, Any
from app.schemas.common import BaseSchema, TimestampSchema

class IntegrationBase(BaseSchema):
    provider: str
    status: str = "ACTIVE"

class IntegrationCreate(IntegrationBase):
    organization_id: str
    config_json: Optional[Dict[str, Any]] = None

class IntegrationRead(IntegrationBase, TimestampSchema):
    config_json: Optional[Dict[str, Any]] = None
    organization_id: str
