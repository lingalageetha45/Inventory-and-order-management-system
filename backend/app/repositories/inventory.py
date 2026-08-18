from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory import Inventory


def get_inventory_by_id(
    db: Session,
    inventory_id: int,
) -> Inventory | None:
    return db.get(Inventory, inventory_id)


def get_inventory_by_product_id(
    db: Session,
    product_id: int,
) -> Inventory | None:
    return db.scalar(
        select(Inventory).where(
            Inventory.product_id == product_id
        )
    )


def get_inventory_list(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[Inventory]:
    return list(
        db.scalars(
            select(Inventory)
            .order_by(Inventory.id)
            .offset(skip)
            .limit(limit)
        ).all()
    )


def get_low_stock_inventory(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[Inventory]:
    return list(
        db.scalars(
            select(Inventory)
            .where(
                Inventory.current_stock
                <= Inventory.minimum_stock_level
            )
            .order_by(Inventory.current_stock)
            .offset(skip)
            .limit(limit)
        ).all()
    )


def create_inventory(
    db: Session,
    inventory: Inventory,
) -> Inventory:
    db.add(inventory)
    db.commit()
    db.refresh(inventory)

    return inventory


def save_inventory(
    db: Session,
    inventory: Inventory,
) -> Inventory:
    db.commit()
    db.refresh(inventory)

    return inventory