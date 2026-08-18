from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.enums.enums import ProductStatus


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None
    category_id: int = Field(gt=0)
    price: Decimal = Field(gt=0)
    sku: str = Field(min_length=2, max_length=100)
    stock_quantity: int = Field(default=0, ge=0)
    status: ProductStatus = ProductStatus.ACTIVE
    image: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    description: str | None = None
    category_id: int | None = Field(
        default=None,
        gt=0,
    )
    price: Decimal | None = Field(
        default=None,
        gt=0,
    )
    sku: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    stock_quantity: int | None = Field(
        default=None,
        ge=0,
    )
    status: ProductStatus | None = None
    image: str | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    category_id: int
    price: Decimal
    sku: str
    stock_quantity: int
    status: ProductStatus
    image: str | None

    model_config = ConfigDict(from_attributes=True)