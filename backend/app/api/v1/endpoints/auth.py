from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from app.core.exceptions import BadRequestException, UnauthorizedException
from app.dependencies.database import get_async_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.organization import Organization
from app.schemas.auth import LoginRequest, RegisterRequest, Token, RefreshTokenRequest
from app.schemas.user import UserRead
from app.schemas.common import GenericResponse

router = APIRouter()

@router.post("/register", response_model=GenericResponse[dict], status_code=status.HTTP_201_CREATED)
async def register(
    req: RegisterRequest,
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    # Check existing user
    stmt = select(User).where(User.email == req.email)
    res = await db.execute(stmt)
    existing_user = res.scalar_one_or_none()
    if existing_user:
        raise BadRequestException("User with this email already exists")

    # Create Organization
    import uuid
    slug_val = req.organization_name.lower().replace(" ", "-") + "-" + str(uuid.uuid4())[:8]
    org = Organization(name=req.organization_name, slug=slug_val)
    db.add(org)
    await db.flush()

    # Create User
    user = User(
        email=req.email,
        hashed_password=get_password_hash(req.password),
        full_name=req.full_name,
        organization_id=org.id,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    return GenericResponse(
        success=True,
        message="Registration successful",
        data={
            "token": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            },
            "user": UserRead.model_validate(user).model_dump(mode="json"),
        }
    )

@router.post("/login", response_model=GenericResponse[dict])
async def login(
    req: LoginRequest,
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    stmt = select(User).where(User.email == req.email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not verify_password(req.password, user.hashed_password):
        raise UnauthorizedException("Invalid email or password")

    if not user.is_active or user.is_deleted:
        raise UnauthorizedException("User account is inactive")

    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    return GenericResponse(
        success=True,
        message="Login successful",
        data={
            "token": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            },
            "user": UserRead.model_validate(user).model_dump(mode="json"),
        }
    )

@router.get("/me", response_model=GenericResponse[UserRead])
async def get_me(current_user: User = Depends(get_current_user)) -> Any:
    return GenericResponse(
        success=True,
        message="User profile retrieved successfully",
        data=UserRead.model_validate(current_user)
    )

@router.post("/logout", response_model=GenericResponse[None])
async def logout(current_user: User = Depends(get_current_user)) -> Any:
    return GenericResponse(
        success=True,
        message="Logged out successfully",
        data=None
    )
