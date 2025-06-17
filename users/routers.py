from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers

from users.auth import UserManager, auth_backend, get_user_manager
from users.models import User
from users.schemas import UserCreate, UserLogin, UserRead, UserUpdate

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

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
    return {"message": "Successfully logged in", "user_id": user.id}
