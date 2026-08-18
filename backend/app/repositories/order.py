from sqlalchemy.orm import Session

from app.models.order import Order


def get_order_by_id(
    db: Session,
    order_id: int,
) -> Order | None:
    return (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )


def get_orders(
    db: Session,
    customer_id: int | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[Order]:
    query = db.query(Order)

    if customer_id is not None:
        query = query.filter(
            Order.customer_id == customer_id
        )

    return (
        query
        .order_by(Order.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_order(
    db: Session,
    order: Order,
) -> Order:
    db.add(order)
    db.flush()
    return order


def update_order(
    db: Session,
    order: Order,
) -> Order:
    db.add(order)
    db.flush()
    return order


def delete_order(
    db: Session,
    order: Order,
) -> None:
    db.delete(order)
    db.flush()