from typing import List, Optional
from sqlalchemy import Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class Forecast(BaseModel):
    __tablename__ = "forecasts"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    horizon_days: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    confidence_interval: Mapped[float] = mapped_column(Float, nullable=False, default=0.95)
    forecast_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    organization: Mapped["Organization"] = relationship("Organization", back_populates="forecasts")

    model_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("ml_models.id", ondelete="SET NULL"), nullable=True
    )
    model: Mapped["MLModel"] = relationship("MLModel", back_populates="forecasts")

    created_by_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    reports: Mapped[List["Report"]] = relationship("Report", back_populates="forecast")
