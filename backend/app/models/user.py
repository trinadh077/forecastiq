from typing import Optional
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    organization_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True
    )
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="users")

    role_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("roles.id", ondelete="SET NULL"), nullable=True
    )
    role: Mapped[Optional["Role"]] = relationship("Role", back_populates="users")
