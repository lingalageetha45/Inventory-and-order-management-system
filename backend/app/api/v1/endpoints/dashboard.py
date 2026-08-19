from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.enums.enums import UserRole
from app.schemas.dashboard import (
    AdminDashboardResponse,
    CustomerDashboardResponse,
    StaffDashboardResponse,
)
from app.services import dashboard as dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/admin",
    response_model=AdminDashboardResponse,
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)
def get_admin_dashboard(
    db: Session = Depends(get_db),
):
    return dashboard_service.get_admin_dashboard(db)


@router.get(
    "/staff",
    response_model=StaffDashboardResponse,
    dependencies=[Depends(require_roles(UserRole.STAFF))],
)
def get_staff_dashboard(
    db: Session = Depends(get_db),
):
    return dashboard_service.get_staff_dashboard(db)


@router.get(
    "/customer",
    response_model=CustomerDashboardResponse,
)
def get_customer_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return dashboard_service.get_customer_dashboard(
        db,
        current_user.id,
    )