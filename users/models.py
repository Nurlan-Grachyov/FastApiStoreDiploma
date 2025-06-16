from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from pydantic import EmailStr
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(150), comment="Напишите свое ФИО")
    phone: Mapped[str] = mapped_column(
        String(12),
        unique=True,
        comment="Введите email или номер телефона. Телефон должен быть в формате +7XXXXXXXXXX",
    )
    email: Mapped[EmailStr] = mapped_column(
        String(100), unique=True, comment="Введите email в формате username@example.com"
    )
    role: Mapped[str] = mapped_column(Enum('superuser', 'admin', 'user',  name="roles"), default="user")

    class Meta:
        table = "users"
