from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.review import Review


def get_review_by_id(
    db: Session,
    review_id: int,
) -> Review | None:
    return db.get(Review, review_id)


def get_reviews(
    db: Session,
    product_id: int | None = None,
) -> list[Review]:
    query = select(Review).order_by(Review.created_at.desc())

    if product_id is not None:
        query = query.where(
            Review.product_id == product_id
        )

    return db.scalars(query).all()


def get_customer_product_order_review(
    db: Session,
    product_id: int,
    customer_id: int,
    order_id: int,
) -> Review | None:
    return db.scalar(
        select(Review).where(
            Review.product_id == product_id,
            Review.customer_id == customer_id,
            Review.order_id == order_id,
        )
    )


def create_review(
    db: Session,
    review: Review,
) -> Review:
    db.add(review)
    db.commit()
    db.refresh(review)

    return review