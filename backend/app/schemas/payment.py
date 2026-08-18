from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.enums.enums import PaymentMethod, PaymentStatus


class PaymentCreate(BaseModel):
    order_id: int
    payment_method: PaymentMethod


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: Decimal
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    payment_date: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentStatusUpdate(BaseModel):
    payment_status: PaymentStatus