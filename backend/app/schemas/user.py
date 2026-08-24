from typing import Optional
from pydantic import EmailStr
from app.schemas.common import BaseSchema, TimestampSchema

class UserBase(BaseSchema):
    email: EmailStr
    full_name: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    organization_id: Optional[str] = None
    role_id: Optional[str] = None

class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserRead(UserBase, TimestampSchema):
    organization_id: Optional[str] = None
    role_id: Optional[str] = None
    is_superuser: bool = False
