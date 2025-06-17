from typing import Any, Optional

from fastapi import Depends, HTTPException, Request
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi_users import BaseUserManager, InvalidID, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import PasswordHelper
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from config.database import get_async_session, get_user_db
from config.settings import SECRET_KEY
from users.models import User
from users.schemas import UserLogin

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

password_hash = PasswordHash((Argon2Hasher(),))
password_helper = PasswordHelper(password_hash)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    USE_CREDENTIALS=settings.USE_CREDENTIALS == "True",
    VALIDATE_CERTS=settings.VALIDATE_CERTS == "True",
    MAIL_STARTTLS=settings.START_TLS == "True",
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS == "True",
)


class UserManager(BaseUserManager[User, int]):
    def __init__(
        self, session: AsyncSession, user_db: BaseUserDatabase[models.UP, models.ID]
    ):
        super().__init__(user_db)
        self.session = session

    def parse_id(self, value: Any) -> int:
        try:
            return int(value)
        except ValueError as e:
            raise InvalidID() from e

    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        message = MessageSchema(
            subject="Регистрация!",
            recipients=[user.email],
            body="Вы успешно зарегистрировались.",
            subtype=MessageType.plain,
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        return {"message": f"Письмо отправлено на {user.email}"}

    async def authenticate(self, credentials: UserLogin):
        if credentials.phone:
            result = await self.session.execute(
                select(User).where(User.phone == credentials.phone)
            )
        elif credentials.email:
            result = await self.session.execute(
                select(User).where(User.email == credentials.email)
            )
        else:
            raise ValueError("Введите номер телефона или email")

        user = result.scalars().first()
        verified, updated_password_hash = password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            raise HTTPException(status_code=401, detail="Неверный пароль")

        if updated_password_hash:
            user.hashed_password = updated_password_hash
            await self.session.commit()

        return user


async def get_user_manager(
    session: AsyncSession = Depends(get_async_session), user_db=Depends(get_user_db)
):
    yield UserManager(session, user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# @router.post("/logout")
# async def logout(response: Response):
#     """Завершаем сеанс пользователя, удаляя cookie с токеном."""
#     print(f"это данные запроса {response.body}")
#     response.delete_cookie("access-token")
#     return {"detail": "Logged out successfully."}
