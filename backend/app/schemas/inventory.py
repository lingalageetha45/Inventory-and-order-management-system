from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InventoryCreate(BaseModel):
    product_id: int
    current_stock: int = Field(default=0, ge=0)
    minimum_stock_level: int = Field(default=0, ge=0)
    maximum_stock_level: int = Field(..., gt=0)


class InventoryUpdate(BaseModel):
    current_stock: int | None = Field(default=None, ge=0)
    minimum_stock_level: int | None = Field(default=None, ge=0)
    maximum_stock_level: int | None = Field(default=None, gt=0)


class StockAdjustment(BaseModel):
    quantity: int = Field(..., gt=0)


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    current_stock: int
    minimum_stock_level: int
    maximum_stock_level: int
    last_updated_at: datetime

    model_config = ConfigDict(from_attributes=True)