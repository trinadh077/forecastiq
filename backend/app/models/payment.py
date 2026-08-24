from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel

class Payment(BaseModel):
    __tablename__ = "payments"

    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD", nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    stripe_payment_intent_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
