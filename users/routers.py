from fastapi import APIRouter, Depends, HTTPException
from fastapi_users.jwt import generate_jwt

from config.settings import SECRET_KEY
from dependencies.fastapi_users_instance import fastapi_users
from users.auth import UserManager, get_user_manager
from users.schemas import UserCreate, UserLogin, UserRead, UserUpdate

user_router = APIRouter(tags=["Users"])


def register_user(app):
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )


def users_router(app):
    app.include_router(
        fastapi_users.get_users_router(
            UserRead, UserUpdate, requires_verification=True
        ),
        prefix="/users",
        tags=["users"],
    )


@user_router.post("/login")
async def login(data: UserLogin, user_manager: UserManager = Depends(get_user_manager)):
    user = await user_manager.authenticate(data)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = generate_jwt({"sub": str(user.id)}, secret=SECRET_KEY, lifetime_seconds=3600)
    return {"access_token": access_token, "token_type": "bearer"}
