from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), comment="Напишите свое ФИО")
    email_or_phone: Mapped[str] = mapped_column(String(100), unique=True,
                                                comment="Введите email или номер телефона. Телефон должен быть в формате +7XXXXXXXXXX")
    password = mapped_column(String(128))
    email: Mapped[str | None] = mapped_column(String(100), nullable=True)

    class Meta:
        table = "users"
