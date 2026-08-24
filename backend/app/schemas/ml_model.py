from typing import Optional, Dict, Any
from app.schemas.common import BaseSchema, TimestampSchema

class MLModelBase(BaseSchema):
    name: str
    algorithm: str

class MLModelCreate(MLModelBase):
    organization_id: str
    dataset_id: str
    hyperparameters: Optional[Dict[str, Any]] = None

class MLModelRead(MLModelBase, TimestampSchema):
    hyperparameters: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    artifact_path: Optional[str] = None
    status: str
    organization_id: str
    dataset_id: str
    created_by_id: Optional[str] = None
