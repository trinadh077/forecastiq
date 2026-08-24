from typing import Optional
from jose import JWTError, jwt
from app.config.settings import settings
from app.core.exceptions import UnauthorizedException
from app.core.redis import redis_service
from app.schemas.auth import TokenPayload

async def decode_token(token: str) -> TokenPayload:
    if await redis_service.is_token_blacklisted(token):
        raise UnauthorizedException("Token has been revoked/logged out")
        
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        sub: Optional[str] = payload.get("sub")
        exp: Optional[int] = payload.get("exp")
        token_type: Optional[str] = payload.get("type", "access")
        
        if sub is None or exp is None:
            raise UnauthorizedException("Invalid token payload")
            
        return TokenPayload(sub=sub, exp=exp, type=token_type)
    except JWTError:
        raise UnauthorizedException("Could not validate credentials")
