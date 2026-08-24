from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
from app.config.constants import SubscriptionPlan

class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    plan_name: Mapped[str] = mapped_column(String(50), default=SubscriptionPlan.STARTER, nullable=False)
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    organization: Mapped["Organization"] = relationship("Organization", back_populates="subscription")
