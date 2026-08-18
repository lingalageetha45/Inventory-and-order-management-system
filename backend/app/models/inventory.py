from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    current_stock: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    minimum_stock_level: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    maximum_stock_level: Mapped[int] = mapped_column(
        nullable=False,
    )

    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="inventory",
    )

    __table_args__ = (
        CheckConstraint(
            "current_stock >= 0",
            name="ck_inventory_current_stock_non_negative",
        ),
        CheckConstraint(
            "minimum_stock_level >= 0",
            name="ck_inventory_minimum_stock_non_negative",
        ),
        CheckConstraint(
            "maximum_stock_level > 0",
            name="ck_inventory_maximum_stock_positive",
        ),
        CheckConstraint(
            "minimum_stock_level <= maximum_stock_level",
            name="ck_inventory_min_max_valid",
        ),
        Index(
            "ix_inventory_low_stock",
            "current_stock",
            "minimum_stock_level",
        ),
    )