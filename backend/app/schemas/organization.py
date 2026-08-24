from typing import Optional, Dict, Any
from app.schemas.common import BaseSchema, TimestampSchema

class OrganizationBase(BaseSchema):
    name: str
    slug: str
    domain: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    settings_json: Optional[Dict[str, Any]] = None

class OrganizationUpdate(BaseSchema):
    name: Optional[str] = None
    domain: Optional[str] = None
    settings_json: Optional[Dict[str, Any]] = None

class OrganizationRead(OrganizationBase, TimestampSchema):
    settings_json: Optional[Dict[str, Any]] = None
