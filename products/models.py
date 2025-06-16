from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func, text, Boolean


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer),
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=text('now()'),
                                                 onupdate=text('now()'))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
