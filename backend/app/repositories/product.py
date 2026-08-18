from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums.enums import ProductStatus
from app.models.product import Product


def get_product_by_id(
    db: Session,
    product_id: int,
) -> Product | None:
    return db.get(Product, product_id)


def get_product_by_sku(
    db: Session,
    sku: str,
) -> Product | None:
    return db.scalar(
        select(Product).where(Product.sku == sku)
    )


def get_products(
    db: Session,
    search: str | None = None,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    status: ProductStatus | None = None,
    active_only: bool = False,
    skip: int = 0,
    limit: int = 20,
) -> list[Product]:
    query = select(Product)

    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.where(
            Product.name.ilike(search_pattern)
            | Product.sku.ilike(search_pattern)
        )

    if category_id is not None:
        query = query.where(
            Product.category_id == category_id
        )

    if min_price is not None:
        query = query.where(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.where(
            Product.price <= max_price
        )

    if status is not None:
        query = query.where(
            Product.status == status
        )

    if active_only:
        query = query.where(
            Product.status == ProductStatus.ACTIVE
        )

    query = (
        query
        .order_by(Product.name)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(query).all())


def create_product(
    db: Session,
    product: Product,
) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product: Product,
) -> None:
    db.delete(product)
    db.commit()