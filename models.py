from tortoise import fields, models

from main import app
from schemas import UserCreate

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, description="Напишите свое ФИО")
    email = fields.CharField(max_length=100, unique=True)
    phone = fields.CharField(max_length=15, description="Телефон в формате +7XXXXXXXXXX")
    password = fields.CharField(max_length=128)


@app.post("/register")
async def register(user: UserCreate):
    hashed_password = hash_password(user.password)
    user_obj = User(
        username=user.username,
        email=user.email,
        phone=user.phone,
        password=hashed_password
    )
    await user_obj.save()
    return {"message": "Пользователь успешно зарегистрирован"}
