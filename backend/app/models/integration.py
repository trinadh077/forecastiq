from typing import Optional
from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel

class Integration(BaseModel):
    __tablename__ = "integrations"

    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # SALESFORCE, HUBSPOT, STRIPE
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)
    config_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
