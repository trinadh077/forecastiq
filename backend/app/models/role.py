from typing import List, Optional
from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class Role(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    permissions_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)

    users: Mapped[List["User"]] = relationship("User", back_populates="role")
