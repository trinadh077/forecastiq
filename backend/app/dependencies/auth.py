from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import decode_token
from app.core.exceptions import UnauthorizedException
from app.dependencies.database import get_async_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
) -> User:
    token_data = await decode_token(token)
    if token_data.type != "access":
        raise UnauthorizedException("Invalid token type")
        
    user = await db.get(User, token_data.sub)
    if not user or not user.is_active or user.is_deleted:
        raise UnauthorizedException("User not found or inactive")
        
    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise UnauthorizedException("Superuser privileges required")
    return current_user
