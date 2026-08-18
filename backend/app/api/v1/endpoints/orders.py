from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from app.enums.enums import UserRole
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.services import order as order_service

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


# ---------------------------------------------------------
# Create Order
# ---------------------------------------------------------
@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.CUSTOMER)
    ),
):
    return order_service.create_order(
        db=db,
        data=data,
        customer_id=current_user.id,
    )


# ---------------------------------------------------------
# List Orders
# Customer -> own orders
# Admin/Staff -> all orders
# ---------------------------------------------------------
@router.get(
    "/",
    response_model=list[OrderResponse],
)
def list_orders(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.CUSTOMER:
        return order_service.list_customer_orders(
            db=db,
            customer_id=current_user.id,
            skip=skip,
            limit=limit,
        )

    if current_user.role in (
        UserRole.ADMIN,
        UserRole.STAFF,
    ):
        return order_service.list_all_orders(
            db=db,
            skip=skip,
            limit=limit,
        )

    return []


# ---------------------------------------------------------
# Get Order
# ---------------------------------------------------------
@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return order_service.get_order_for_user(
        db=db,
        order_id=order_id,
        current_user=current_user,
    )


# ---------------------------------------------------------
# Confirm Order
# Pending -> Confirmed
# ---------------------------------------------------------
@router.put(
    "/{order_id}/confirm",
    response_model=OrderResponse,
)
def confirm_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.STAFF,
        )
    ),
):
    return order_service.confirm_order(
        db=db,
        order_id=order_id,
    )


# ---------------------------------------------------------
# Ship Order
# Confirmed -> Shipped
# ---------------------------------------------------------
@router.put(
    "/{order_id}/ship",
    response_model=OrderResponse,
)
def ship_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.STAFF,
        )
    ),
):
    return order_service.ship_order(
        db=db,
        order_id=order_id,
    )


# ---------------------------------------------------------
# Deliver Order
# Shipped -> Delivered
# ---------------------------------------------------------
@router.put(
    "/{order_id}/deliver",
    response_model=OrderResponse,
)
def deliver_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.STAFF,
        )
    ),
):
    return order_service.deliver_order(
        db=db,
        order_id=order_id,
    )


# ---------------------------------------------------------
# Cancel Order
# ---------------------------------------------------------
@router.put(
    "/{order_id}/cancel",
    response_model=OrderResponse,
)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return order_service.cancel_order(
        db=db,
        order_id=order_id,
        current_user=current_user,
    )