from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.enums.enums import UserRole
from app.models.user import User
from app.repositories import order as order_repository
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentStatusUpdate,
)
from app.services import payment as payment_service


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.CUSTOMER)
    ),
):
    order = order_repository.get_order_by_id(
        db,
        data.order_id,
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    if order.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only pay for your own orders",
        )

    return payment_service.create_payment(
        db=db,
        order_id=data.order_id,
        amount=order.total_amount,
        payment_method=data.payment_method,
    )


@router.get(
    "/",
    response_model=list[PaymentResponse],
)
def list_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN, UserRole.STAFF)
    ),
):
    return payment_service.list_payments(db)


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN, UserRole.STAFF)
    ),
):
    return payment_service.get_payment(
        db,
        payment_id,
    )


@router.patch(
    "/{payment_id}/status",
    response_model=PaymentResponse,
)
def update_payment_status(
    payment_id: int,
    data: PaymentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN, UserRole.STAFF)
    ),
):
    return payment_service.update_payment_status(
        db,
        payment_id,
        data.payment_status,
    )