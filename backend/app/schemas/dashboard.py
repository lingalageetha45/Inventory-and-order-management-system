from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AdminDashboardResponse(BaseModel):
    total_customers: int
    total_staff: int
    total_products: int
    total_categories: int
    total_orders: int
    pending_orders: int
    completed_orders: int
    cancelled_orders: int
    low_stock_products: int
    total_revenue: Decimal

    model_config = ConfigDict(from_attributes=True)


class StaffDashboardResponse(BaseModel):
    total_products: int
    low_stock_products: int
    todays_orders: int
    pending_orders: int
    completed_orders: int

    model_config = ConfigDict(from_attributes=True)


class CustomerDashboardResponse(BaseModel):
    total_orders: int
    pending_orders: int
    completed_orders: int
    cancelled_orders: int
    total_amount_spent: Decimal

    model_config = ConfigDict(from_attributes=True)