from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class Report(BaseModel):
    __tablename__ = "reports"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    report_type: Mapped[str] = mapped_column(String(50), nullable=False)  # PDF, EXCEL
    file_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    
    forecast_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("forecasts.id", ondelete="CASCADE"), nullable=True
    )
    forecast: Mapped[Optional["Forecast"]] = relationship("Forecast", back_populates="reports")
