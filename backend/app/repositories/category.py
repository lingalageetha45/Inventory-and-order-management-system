from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


def get_category_by_id(
    db: Session,
    category_id: int,
) -> Category | None:
    return db.get(Category, category_id)


def get_category_by_name(
    db: Session,
    name: str,
) -> Category | None:
    return db.scalar(
        select(Category).where(
            Category.name.ilike(name.strip())
        )
    )


def get_categories(
    db: Session,
    search: str | None = None,
    status=None,
    skip: int = 0,
    limit: int = 20,
) -> list[Category]:
    query = select(Category)

    if search:
        query = query.where(
            Category.name.ilike(
                f"%{search.strip()}%"
            )
        )

    if status is not None:
        query = query.where(
            Category.status == status
        )

    query = (
        query
        .order_by(Category.name)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(query).all())


def create_category(
    db: Session,
    category: Category,
) -> Category:
    db.add(category)
    db.commit()
    db.refresh(category)
    return category