from pydantic import EmailStr
from app.schemas.common import BaseSchema
from app.schemas.user import UserRead

class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseSchema):
    sub: str
    exp: int
    type: str

class LoginRequest(BaseSchema):
    email: EmailStr
    password: str

class RegisterRequest(BaseSchema):
    email: EmailStr
    password: str
    full_name: str
    organization_name: str

class RefreshTokenRequest(BaseSchema):
    refresh_token: str
