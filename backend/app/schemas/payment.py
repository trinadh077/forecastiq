from typing import Optional
from app.schemas.common import BaseSchema, TimestampSchema

class PaymentBase(BaseSchema):
    amount_cents: int
    currency: str = "USD"
    status: str

class PaymentCreate(PaymentBase):
    organization_id: str
    stripe_payment_intent_id: Optional[str] = None

class PaymentRead(PaymentBase, TimestampSchema):
    stripe_payment_intent_id: Optional[str] = None
    organization_id: str
