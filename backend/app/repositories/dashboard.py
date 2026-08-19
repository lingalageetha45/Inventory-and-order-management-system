from datetime import datetime, time
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.enums.enums import OrderStatus, PaymentStatus, UserRole
from app.models.category import Category
from app.models.inventory import Inventory
from app.models.order import Order
from app.models.payment import Payment
from app.models.product import Product
from app.models.user import User


def get_admin_dashboard(db: Session) -> dict:
    total_customers = (
        db.query(func.count(User.id))
        .filter(User.role == UserRole.CUSTOMER)
        .scalar()
        or 0
    )

    total_staff = (
        db.query(func.count(User.id))
        .filter(User.role == UserRole.STAFF)
        .scalar()
        or 0
    )

    total_products = db.query(func.count(Product.id)).scalar() or 0
    total_categories = db.query(func.count(Category.id)).scalar() or 0
    total_orders = db.query(func.count(Order.id)).scalar() or 0

    pending_orders = (
        db.query(func.count(Order.id))
        .filter(Order.status == OrderStatus.PENDING)
        .scalar()
        or 0
    )

    completed_orders = (
        db.query(func.count(Order.id))
        .filter(Order.status == OrderStatus.DELIVERED)
        .scalar()
        or 0
    )

    cancelled_orders = (
        db.query(func.count(Order.id))
        .filter(Order.status == OrderStatus.CANCELLED)
        .scalar()
        or 0
    )

    low_stock_products = (
        db.query(func.count(Inventory.id))
        .filter(
            Inventory.current_stock
            <= Inventory.minimum_stock_level
        )
        .scalar()
        or 0
    )

    total_revenue = (
        db.query(func.coalesce(func.sum(Payment.amount), 0))
        .filter(Payment.payment_status == PaymentStatus.PAID)
        .scalar()
        or Decimal("0.00")
    )

    return {
        "total_customers": total_customers,
        "total_staff": total_staff,
        "total_products": total_products,
        "total_categories": total_categories,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "low_stock_products": low_stock_products,
        "total_revenue": total_revenue,
    }


def get_staff_dashboard(db: Session) -> dict:
    today = datetime.now().date()

    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    total_products = db.query(func.count(Product.id)).scalar() or 0

    low_stock_products = (
        db.query(func.count(Inventory.id))
        .filter(
            Inventory.current_stock
            <= Inventory.minimum_stock_level
        )
        .scalar()
        or 0
    )

    todays_orders = (
        db.query(func.count(Order.id))
        .filter(
            Order.created_at >= start_of_day,
            Order.created_at <= end_of_day,
        )
        .scalar()
        or 0
    )

    pending_orders = (
        db.query(func.count(Order.id))
        .filter(Order.status == OrderStatus.PENDING)
        .scalar()
        or 0
    )

    completed_orders = (
        db.query(func.count(Order.id))
        .filter(Order.status == OrderStatus.DELIVERED)
        .scalar()
        or 0
    )

    return {
        "total_products": total_products,
        "low_stock_products": low_stock_products,
        "todays_orders": todays_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
    }


def get_customer_dashboard(
    db: Session,
    customer_id: int,
) -> dict:
    total_orders = (
        db.query(func.count(Order.id))
        .filter(Order.customer_id == customer_id)
        .scalar()
        or 0
    )

    pending_orders = (
        db.query(func.count(Order.id))
        .filter(
            Order.customer_id == customer_id,
            Order.status == OrderStatus.PENDING,
        )
        .scalar()
        or 0
    )

    completed_orders = (
        db.query(func.count(Order.id))
        .filter(
            Order.customer_id == customer_id,
            Order.status == OrderStatus.DELIVERED,
        )
        .scalar()
        or 0
    )

    cancelled_orders = (
        db.query(func.count(Order.id))
        .filter(
            Order.customer_id == customer_id,
            Order.status == OrderStatus.CANCELLED,
        )
        .scalar()
        or 0
    )

    total_amount_spent = (
        db.query(func.coalesce(func.sum(Order.total_amount), 0))
        .filter(
            Order.customer_id == customer_id,
            Order.status != OrderStatus.CANCELLED,
        )
        .scalar()
        or Decimal("0.00")
    )

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "total_amount_spent": total_amount_spent,
    }