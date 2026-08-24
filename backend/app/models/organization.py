from typing import List, Optional
from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class Organization(BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    settings_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)

    users: Mapped[List["User"]] = relationship("User", back_populates="organization")
    datasets: Mapped[List["Dataset"]] = relationship("Dataset", back_populates="organization")
    models: Mapped[List["MLModel"]] = relationship("MLModel", back_populates="organization")
    forecasts: Mapped[List["Forecast"]] = relationship("Forecast", back_populates="organization")
    subscription: Mapped[Optional["Subscription"]] = relationship("Subscription", back_populates="organization", uselist=False)
