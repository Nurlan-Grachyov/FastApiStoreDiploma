from decimal import Decimal

from sqlalchemy import DECIMAL, Boolean, DateTime, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), onupdate=text("now()")
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
