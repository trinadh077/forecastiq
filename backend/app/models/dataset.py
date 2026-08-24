from typing import List, Optional
from sqlalchemy import BigInteger, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
from app.config.constants import DatasetStatus

class Dataset(BaseModel):
    __tablename__ = "datasets"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    row_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    column_schema: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default=DatasetStatus.PENDING, nullable=False)

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    organization: Mapped["Organization"] = relationship("Organization", back_populates="datasets")

    uploaded_by_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    models: Mapped[List["MLModel"]] = relationship("MLModel", back_populates="dataset")
