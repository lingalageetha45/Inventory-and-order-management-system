from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.product import Product
from app.repositories import inventory as inventory_repository
from app.repositories import product as product_repository
from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
)


def list_inventory(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[Inventory]:
    return inventory_repository.get_inventory_list(
        db,
        skip=skip,
        limit=limit,
    )


def list_low_stock(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[Inventory]:
    return inventory_repository.get_low_stock_inventory(
        db,
        skip=skip,
        limit=limit,
    )


def get_inventory(
    db: Session,
    inventory_id: int,
) -> Inventory:
    inventory = inventory_repository.get_inventory_by_id(
        db,
        inventory_id,
    )

    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found",
        )

    return inventory


def get_inventory_by_product_id(
    db: Session,
    product_id: int,
) -> Inventory:
    inventory = (
        inventory_repository.get_inventory_by_product_id(
            db,
            product_id,
        )
    )

    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found for this product",
        )

    return inventory


def _get_product(
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


def create_inventory(
    db: Session,
    data: InventoryCreate,
) -> Inventory:
    product = _get_product(
        db,
        data.product_id,
    )

    existing = (
        inventory_repository.get_inventory_by_product_id(
            db,
            data.product_id,
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Inventory already exists for this product",
        )

    if data.maximum_stock_level < data.minimum_stock_level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Maximum stock level must be greater than "
                "or equal to minimum stock level"
            ),
        )

    if data.current_stock > data.maximum_stock_level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current stock cannot exceed maximum stock level",
        )

    inventory = Inventory(
        product_id=data.product_id,
        current_stock=data.current_stock,
        minimum_stock_level=data.minimum_stock_level,
        maximum_stock_level=data.maximum_stock_level,
    )

    product.stock_quantity = data.current_stock

    return inventory_repository.create_inventory(
        db,
        inventory,
    )


def update_inventory(
    db: Session,
    inventory_id: int,
    data: InventoryUpdate,
) -> Inventory:
    inventory = get_inventory(
        db,
        inventory_id,
    )

    updates = data.model_dump(
        exclude_unset=True,
    )

    current_stock = updates.get(
        "current_stock",
        inventory.current_stock,
    )

    minimum_stock_level = updates.get(
        "minimum_stock_level",
        inventory.minimum_stock_level,
    )

    maximum_stock_level = updates.get(
        "maximum_stock_level",
        inventory.maximum_stock_level,
    )

    if maximum_stock_level < minimum_stock_level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Maximum stock level must be greater than "
                "or equal to minimum stock level"
            ),
        )

    if current_stock > maximum_stock_level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current stock cannot exceed maximum stock level",
        )

    for field, value in updates.items():
        setattr(inventory, field, value)

    product = _get_product(
        db,
        inventory.product_id,
    )

    product.stock_quantity = current_stock

    return inventory_repository.save_inventory(
        db,
        inventory,
    )


def add_stock(
    db: Session,
    product_id: int,
    quantity: int,
) -> Inventory:
    inventory = get_inventory_by_product_id(
        db,
        product_id,
    )

    product = _get_product(
        db,
        product_id,
    )

    new_stock = inventory.current_stock + quantity

    if new_stock > inventory.maximum_stock_level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock quantity cannot exceed maximum stock level",
        )

    inventory.current_stock = new_stock
    product.stock_quantity = new_stock

    return inventory_repository.save_inventory(
        db,
        inventory,
    )


def remove_stock(
    db: Session,
    product_id: int,
    quantity: int,
) -> Inventory:
    inventory = get_inventory_by_product_id(
        db,
        product_id,
    )

    product = _get_product(
        db,
        product_id,
    )

    if quantity > inventory.current_stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock",
        )

    inventory.current_stock -= quantity
    product.stock_quantity = inventory.current_stock

    return inventory_repository.save_inventory(
        db,
        inventory,
    )