from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories import category as category_repository


def create_category(
    db: Session,
    name: str,
    description: str | None = None,
    category_status=None,
) -> Category:
    existing = category_repository.get_category_by_name(
        db,
        name,
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this name already exists",
        )

    category = Category(
        name=name.strip(),
        description=description,
        status=category_status,
    )

    return category_repository.create_category(
        db,
        category,
    )


def get_category(
    db: Session,
    category_id: int,
) -> Category:
    category = category_repository.get_category_by_id(
        db,
        category_id,
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


def list_categories(
    db: Session,
    search: str | None = None,
    category_status=None,
    skip: int = 0,
    limit: int = 20,
) -> list[Category]:
    return category_repository.get_categories(
        db,
        search=search,
        status=category_status,
        skip=skip,
        limit=limit,
    )


def update_category(
    db: Session,
    category_id: int,
    update_data: dict,
) -> Category:
    category = get_category(
        db,
        category_id,
    )

    if "name" in update_data and update_data["name"]:
        existing = category_repository.get_category_by_name(
            db,
            update_data["name"],
        )

        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category with this name already exists",
            )

    for field, value in update_data.items():
        if value is not None:
            setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category_id: int,
) -> None:
    category = get_category(
        db,
        category_id,
    )

    if category.products:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete category containing products",
        )

    db.delete(category)
    db.commit()