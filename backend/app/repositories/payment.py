from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import Payment


def get_payment_by_id(
    db: Session,
    payment_id: int,
) -> Payment | None:
    return db.get(Payment, payment_id)


def get_payment_by_order_id(
    db: Session,
    order_id: int,
) -> Payment | None:
    return db.scalar(
        select(Payment).where(
            Payment.order_id == order_id
        )
    )


def get_payments(
    db: Session,
) -> list[Payment]:
    return db.scalars(
        select(Payment).order_by(Payment.payment_date.desc())
    ).all()


def create_payment(
    db: Session,
    payment: Payment,
) -> Payment:
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment