from datetime import datetime
from pydantic import BaseModel, Field
from app.models.payment import PaymentStatus


class PaymentCreate(BaseModel):
    order_id: int
    amount: float = Field(gt=0)
    currency: str = "USD"


class PaymentRead(BaseModel):
    id: int
    order_id: int
    amount: float
    currency: str
    status: PaymentStatus
    provider: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
