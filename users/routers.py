from fastapi_users import FastAPIUsers

from users.auth import auth_backend, get_user_manager
from users.models import User
from users.schemas import UserCreate, UserRead, UserUpdate

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


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
