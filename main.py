from datetime import timedelta, datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise
from jose import jwt

from models import User, hash_password
from schemas import Token, UserCreate
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, DATABASE_URL, SECRET_KEY, ALGORITHM

app = FastAPI()


@app.post("/register/", response_model=UserCreate)
async def register(user_in: UserCreate):
    """Регистрирует нового пользователя."""
    existing_user = await User.filter(email_or_phone=user_in.email_or_phone).exists()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or phone already exists.")

    hashed_password = hash_password(user_in.password)
    user = await User.create(
        username=user_in.username,
        password=hashed_password,
        email_or_phone=user_in.email_or_phone,
    )
    return user


@app.post("/token/", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    """ Осуществляет вход пользователя и выдаёт JWT-токен. Пользователь вводит свои учётные данные (имя пользователя или телефон и пароль), после успешной аутентификации возвращается JWT-токен. """
    # Поиск пользователя по имени пользователя или телефону
    user = await crud_user.get_by_username_or_phone(session, form_data.username)

    # Аутентификация пользователя
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Генерация JWT-токена
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user.username,
        "exp": datetime.utcnow() + access_token_expires
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer"}


@app.get("/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Возвращает данные текущего залогиненного пользователя."""
    return current_user


# Регистрация Tortoise ORM
register_tortoise(
    app, db_url=DATABASE_URL, modules={"models": ["__main__"]}, generate_schemas=True
)
