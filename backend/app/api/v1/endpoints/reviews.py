from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.enums.enums import UserRole
from app.models.user import User
from app.schemas.review import (
    ReviewCreate,
    ReviewResponse,
)
from app.services import review as review_service


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.CUSTOMER)
    ),
):
    return review_service.create_review(
        db=db,
        customer_id=current_user.id,
        product_id=data.product_id,
        order_id=data.order_id,
        rating=data.rating,
        review_text=data.review,
    )


@router.get(
    "/",
    response_model=list[ReviewResponse],
)
def list_reviews(
    product_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.list_reviews(
        db,
        product_id=product_id,
    )


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.get_review(
        db,
        review_id,
    )