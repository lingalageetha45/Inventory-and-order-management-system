from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums.enums import OrderStatus, PaymentStatus
from app.models.payment import Payment
from app.repositories import order as order_repository
from app.repositories import payment as payment_repository


ALLOWED_PAYMENT_TRANSITIONS = {
    PaymentStatus.PENDING: {
        PaymentStatus.PAID,
        PaymentStatus.FAILED,
    },
    PaymentStatus.PAID: set(),
    PaymentStatus.FAILED: {
        PaymentStatus.PENDING,
    },
}


def list_payments(
    db: Session,
) -> list[Payment]:
    return payment_repository.get_payments(db)


def get_payment(
    db: Session,
    payment_id: int,
) -> Payment:
    payment = payment_repository.get_payment_by_id(
        db,
        payment_id,
    )

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    return payment


def create_payment(
    db: Session,
    order_id: int,
    amount: Decimal,
    payment_method,
) -> Payment:
    order = order_repository.get_order_by_id(
        db,
        order_id,
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    existing_payment = payment_repository.get_payment_by_order_id(
        db,
        order_id,
    )

    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already exists for this order",
        )

    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot pay for a cancelled order",
        )

    if order.status == OrderStatus.DELIVERED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create payment for a delivered order",
        )

    if amount <= Decimal("0"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount must be greater than zero",
        )

    if amount != order.total_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount must match the order total",
        )

    payment = Payment(
        order_id=order_id,
        amount=amount,
        payment_method=payment_method,
        payment_status=PaymentStatus.PENDING,
    )

    return payment_repository.create_payment(
        db,
        payment,
    )


def update_payment_status(
    db: Session,
    payment_id: int,
    payment_status: PaymentStatus,
) -> Payment:
    payment = get_payment(
        db,
        payment_id,
    )

    if payment.payment_status == payment_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already has this status",
        )

    allowed_statuses = ALLOWED_PAYMENT_TRANSITIONS.get(
        payment.payment_status,
        set(),
    )

    if payment_status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Invalid payment status transition: "
                f"{payment.payment_status.value} "
                f"-> {payment_status.value}"
            ),
        )

    order = order_repository.get_order_by_id(
        db,
        payment.order_id,
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated order not found",
        )

    if (
        payment_status == PaymentStatus.PAID
        and order.status == OrderStatus.CANCELLED
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot mark payment as paid for a cancelled order",
        )

    payment.payment_status = payment_status

    if (
        payment_status == PaymentStatus.PAID
        and order.status == OrderStatus.PENDING
    ):
        order.status = OrderStatus.CONFIRMED

    db.commit()
    db.refresh(payment)

    return payment