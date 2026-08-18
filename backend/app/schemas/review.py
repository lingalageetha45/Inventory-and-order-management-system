from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    product_id: int
    order_id: int
    rating: int = Field(..., ge=1, le=5)
    review: str = Field(..., min_length=1, max_length=2000)


class ReviewResponse(BaseModel):
    id: int
    product_id: int
    customer_id: int
    order_id: int
    rating: int
    review: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewUpdate(BaseModel):
    rating: int | None = Field(None, ge=1, le=5)
    review: str | None = Field(None, min_length=1, max_length=2000)