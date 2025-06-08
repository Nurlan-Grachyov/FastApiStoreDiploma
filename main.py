from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise

from auth import (authenticate_user, create_access_token, get_current_user,
                  hash_password)
from models import User
from schemas import Token, UserCreate
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, DATABASE_URL

app = FastAPI()


@app.post("/register/", response_model=UserCreate)
async def register(user_in: UserCreate):
    """Регистрирует нового пользователя."""
    existing_user = await User.filter(email_or_phone=user_in.email_or_phone).exists()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or phone already exists.")

    hashed_password = await hash_password(user_in.password)
    user = await User.create(
        username=user_in.username,
        password_hash=hashed_password,
        email_or_phone=user_in.email_or_phone,
    )
    return user


@app.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Осуществляет вход пользователя и выдает JWT-токен."""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email/phone or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Возвращает данные текущего залогиненного пользователя."""
    return current_user


# Регистрация Tortoise ORM
register_tortoise(
    app, db_url=DATABASE_URL, modules={"models": ["__main__"]}, generate_schemas=True
)


