from typing import Optional, Dict, Any
from app.schemas.common import BaseSchema, TimestampSchema

class AuditLogBase(BaseSchema):
    action: str
    resource_type: str
    details: Optional[Dict[str, Any]] = None

class AuditLogCreate(AuditLogBase):
    organization_id: str
    user_id: Optional[str] = None

class AuditLogRead(AuditLogBase, TimestampSchema):
    user_id: Optional[str] = None
    organization_id: str
