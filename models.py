from passlib.context import CryptContext
from pydantic import EmailStr
from tortoise import fields
from fastapi_users_db_tortoise import TortoiseBaseUserModel

from main import app
from schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class User(TortoiseBaseUserModel):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, description="Напишите свое ФИО")
    email_or_phone: EmailStr | str = fields.CharField(..., unique=True,
                                                      description="Введите email или номер телефона. Телефон должен быть в формате +7XXXXXXXXXX")
    password = fields.CharField(max_length=128)

    class Meta:
        table = "users"


@app.post("/register")
async def register(user: UserCreate):
    hashed_password = hash_password(user.password)
    user_obj = User(
        username=user.username,
        email=user.email,
        phone=user.phone,
        password=hashed_password,
    )
    await user_obj.save()
    return {"message": "Пользователь успешно зарегистрирован"}
