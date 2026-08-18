from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums.enums import ProductStatus
from app.models.product import Product
from app.repositories import product as product_repository


def create_product(
    db: Session,
    name: str,
    description: str | None,
    category_id: int,
    price: Decimal,
    sku: str,
    stock_quantity: int,
    product_status: ProductStatus,
    image: str | None = None,
) -> Product:
    existing_product = product_repository.get_product_by_sku(
        db,
        sku,
    )

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with this SKU already exists",
        )

    product = Product(
        name=name,
        description=description,
        category_id=category_id,
        price=price,
        sku=sku,
        stock_quantity=stock_quantity,
        status=product_status,
        image=image,
    )

    return product_repository.create_product(
        db,
        product,
    )


def get_product(
    db: Session,
    product_id: int,
) -> Product:
    product = product_repository.get_product_by_id(
        db,
        product_id,
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


def list_products(
    db: Session,
    search: str | None = None,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    product_status: ProductStatus | None = None,
    active_only: bool = False,
    skip: int = 0,
    limit: int = 20,
) -> list[Product]:

    if min_price is not None and max_price is not None:
        if min_price > max_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum price cannot be greater than maximum price",
            )

    return product_repository.get_products(
        db,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        status=product_status,
        active_only=active_only,
        skip=skip,
        limit=limit,
    )


def update_product(
    db: Session,
    product_id: int,
    update_data: dict,
) -> Product:
    product = get_product(
        db,
        product_id,
    )

    if "sku" in update_data:
        existing_product = product_repository.get_product_by_sku(
            db,
            update_data["sku"],
        )

        if (
            existing_product
            and existing_product.id != product_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product with this SKU already exists",
            )

    for field, value in update_data.items():
        if value is not None:
            setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product_id: int,
) -> None:
    product = get_product(
        db,
        product_id,
    )

    product_repository.delete_product(
        db,
        product,
    )