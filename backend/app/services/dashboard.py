from sqlalchemy.orm import Session

from app.repositories import dashboard as dashboard_repository


def get_admin_dashboard(db: Session) -> dict:
    return dashboard_repository.get_admin_dashboard(db)


def get_staff_dashboard(db: Session) -> dict:
    return dashboard_repository.get_staff_dashboard(db)


def get_customer_dashboard(
    db: Session,
    customer_id: int,
) -> dict:
    return dashboard_repository.get_customer_dashboard(
        db,
        customer_id,
    )