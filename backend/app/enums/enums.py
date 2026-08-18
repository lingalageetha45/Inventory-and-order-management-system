from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    CUSTOMER = "customer"


class ProductStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CategoryStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethod(str, Enum):
    CARD = "card"
    UPI = "upi"
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"