from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums.enums import OrderStatus, ProductStatus
from app.models.inventory import Inventory
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories import order as order_repository
from app.repositories import product as product_repository
from app.schemas.order import OrderCreate


ALLOWED_TRANSITIONS = {
    OrderStatus.PENDING: {
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.CONFIRMED: {
        OrderStatus.SHIPPED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.SHIPPED: {
        OrderStatus.DELIVERED,
    },
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set(),
}


def list_orders(
    db: Session,
    customer_id: int | None = None,
) -> list[Order]:
    return order_repository.get_orders(
        db,
        customer_id=customer_id,
    )


def get_order(
    db: Session,
    order_id: int,
) -> Order:
    order = order_repository.get_order_by_id(
        db,
        order_id,
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order


def create_order(
    db: Session,
    customer_id: int,
    data: OrderCreate,
) -> Order:
    if not data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item",
        )

    product_ids = [
        item.product_id
        for item in data.items
    ]

    if len(product_ids) != len(set(product_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A product cannot appear more than once in an order",
        )

    order = Order(
        customer_id=customer_id,
        total_amount=Decimal("0.00"),
        status=OrderStatus.PENDING,
    )

    db.add(order)
    db.flush()

    total_amount = Decimal("0.00")

    try:
        for item_data in data.items:
            if item_data.quantity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Quantity must be greater than zero",
                )

            product = product_repository.get_product_by_id(
                db,
                item_data.product_id,
            )

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=(
                        f"Product {item_data.product_id} not found"
                    ),
                )

            if product.status != ProductStatus.ACTIVE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {product.id} is inactive",
                )

            inventory = db.query(Inventory).filter(
                Inventory.product_id == product.id
            ).with_for_update().first()

            if not inventory:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=(
                        f"Inventory not found for product {product.id}"
                    ),
                )

            if inventory.current_stock < item_data.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Insufficient stock for product {product.id}"
                    ),
                )

            unit_price = Decimal(product.price)
            subtotal = unit_price * item_data.quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item_data.quantity,
                unit_price=unit_price,
                subtotal=subtotal,
            )

            db.add(order_item)

            inventory.current_stock -= item_data.quantity

            product.stock_quantity = inventory.current_stock

            total_amount += subtotal

        order.total_amount = total_amount

        db.commit()
        db.refresh(order)

        return order

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create order",
        )


def update_order_status(
    db: Session,
    order_id: int,
    new_status: OrderStatus,
) -> Order:
    order = get_order(db, order_id)

    allowed_statuses = ALLOWED_TRANSITIONS.get(
        order.status,
        set(),
    )

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Invalid order status transition: "
                f"{order.status.value} -> {new_status.value}"
            ),
        )

    order.status = new_status

    db.commit()
    db.refresh(order)

    return order


def cancel_order(
    db: Session,
    order_id: int,
) -> Order:
    order = get_order(db, order_id)

    if order.status not in {
        OrderStatus.PENDING,
        OrderStatus.CONFIRMED,
    }:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only pending or confirmed orders "
                "can be cancelled"
            ),
        )

    for item in order.items:
        inventory = db.query(Inventory).filter(
            Inventory.product_id == item.product_id
        ).with_for_update().first()

        if inventory:
            inventory.current_stock += item.quantity

            product = product_repository.get_product_by_id(
                db,
                item.product_id,
            )

            if product:
                product.stock_quantity = (
                    inventory.current_stock
                )

    order.status = OrderStatus.CANCELLED

    db.commit()
    db.refresh(order)

    return order