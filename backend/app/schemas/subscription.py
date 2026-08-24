from typing import Optional
from app.schemas.common import BaseSchema, TimestampSchema

class SubscriptionBase(BaseSchema):
    plan_name: str
    status: str = "ACTIVE"

class SubscriptionCreate(SubscriptionBase):
    organization_id: str
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None

class SubscriptionRead(SubscriptionBase, TimestampSchema):
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    organization_id: str
