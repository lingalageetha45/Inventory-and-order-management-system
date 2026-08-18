from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from app.enums.enums import UserRole
from app.models.user import User
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse,
    InventoryUpdate,
    StockAdjustment,
)
from app.services import inventory as inventory_service


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


# ---------------------------------------------------------
# List Inventory
# ---------------------------------------------------------
@router.get(
    "/",
    response_model=list[InventoryResponse],
)
def list_inventory(
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
    return inventory_service.list_inventory(
        db,
        skip=skip,
        limit=limit,
    )


# ---------------------------------------------------------
# Low Stock Inventory
# IMPORTANT: Keep this BEFORE /{product_id}
# ---------------------------------------------------------
@router.get(
    "/low-stock",
    response_model=list[InventoryResponse],
)
def low_stock_inventory(
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
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.STAFF,
        )
    ),
):
    return inventory_service.list_low_stock(
        db,
        skip=skip,
        limit=limit,
    )


# ---------------------------------------------------------
# Create Inventory
# ---------------------------------------------------------
@router.post(
    "/",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_inventory(
    data: InventoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.STAFF,
        )
    ),
):
    return inventory_service.create_inventory(
        db,
        data,
    )


# ---------------------------------------------------------
# Get Inventory By Product
# ---------------------------------------------------------
@router.get(
    "/{product_id}",
    response_model=InventoryResponse,
)
def get_inventory(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return inventory_service.get_inventory_by_product_id(
        db,
        product_id,
    )


# ---------------------------------------------------------
# Update Inventory
# ---------------------------------------------------------
@router.put(
    "/{product_id}",
    response_model=InventoryResponse,
)
def update_inventory(
    product_id: int,
    data: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.STAFF,
        )
    ),
):
    inventory = inventory_service.get_inventory_by_product_id(
        db,
        product_id,
    )

    return inventory_service.update_inventory(
        db,
        inventory.id,
        data,
    )


# ---------------------------------------------------------
# Add Stock
# ---------------------------------------------------------
@router.post(
    "/{product_id}/add-stock",
    response_model=InventoryResponse,
)
def add_stock(
    product_id: int,
    data: StockAdjustment,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.STAFF,
        )
    ),
):
    if data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero",
        )

    return inventory_service.add_stock(
        db,
        product_id,
        data.quantity,
    )


# ---------------------------------------------------------
# Remove Stock
# ---------------------------------------------------------
@router.post(
    "/{product_id}/remove-stock",
    response_model=InventoryResponse,
)
def remove_stock(
    product_id: int,
    data: StockAdjustment,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.STAFF,
        )
    ),
):
    if data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero",
        )

    return inventory_service.remove_stock(
        db,
        product_id,
        data.quantity,
    )