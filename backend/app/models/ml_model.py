from typing import List, Optional
from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
from app.config.constants import ModelStatus

class MLModel(BaseModel):
    __tablename__ = "ml_models"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    algorithm: Mapped[str] = mapped_column(String(50), nullable=False)
    hyperparameters: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    metrics: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    artifact_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default=ModelStatus.TRAINING, nullable=False)

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    organization: Mapped["Organization"] = relationship("Organization", back_populates="models")

    dataset_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False
    )
    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="models")

    created_by_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    forecasts: Mapped[List["Forecast"]] = relationship("Forecast", back_populates="model")
