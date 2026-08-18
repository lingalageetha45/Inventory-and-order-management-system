from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums.enums import OrderStatus
from app.models.review import Review
from app.repositories import order as order_repository
from app.repositories import review as review_repository
from app.repositories import product as product_repository


def list_reviews(
    db: Session,
    product_id: int | None = None,
) -> list[Review]:
    return review_repository.get_reviews(
        db,
        product_id=product_id,
    )


def get_review(
    db: Session,
    review_id: int,
) -> Review:
    review = review_repository.get_review_by_id(
        db,
        review_id,
    )

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    return review


def create_review(
    db: Session,
    customer_id: int,
    product_id: int,
    order_id: int,
    rating: int,
    review_text: str,
) -> Review:
    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5",
        )

    product = product_repository.get_product_by_id(
        db,
        product_id,
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    order = order_repository.get_order_by_id(
        db,
        order_id,
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    if order.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only review your own orders",
        )

    if order.status != OrderStatus.DELIVERED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "You can review a product only after "
                "the order is delivered"
            ),
        )

    order_item = order_repository.get_order_item(
        db,
        order_id,
        product_id,
    )

    if not order_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only review products included in the order",
        )

    existing_review = (
        review_repository.get_customer_product_order_review(
            db,
            product_id,
            customer_id,
            order_id,
        )
    )

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "You have already reviewed this product "
                "for this order"
            ),
        )

    review = Review(
        product_id=product_id,
        customer_id=customer_id,
        order_id=order_id,
        rating=rating,
        review=review_text,
    )

    return review_repository.create_review(
        db,
        review,
    )