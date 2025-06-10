import uuid

from fastapi_users import FastAPIUsers

from auth import auth_backend, get_user_manager
from main import app
from users.models import User

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)
