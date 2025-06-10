from typing import Any

from fastapi_mail import ConnectionConfig
from fastapi_users import InvalidID, BaseUserManager, models
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import PasswordHelper
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

import settings

from settings import SECRET_KEY

import bcrypt
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session, get_user_db
from users.models import User
from users.schemas import UserCreate, UserLogin

password_hash = PasswordHash((Argon2Hasher(),))
password_helper = PasswordHelper(password_hash)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    USE_CREDENTIALS=settings.USE_CREDENTIALS == "True",
    VALIDATE_CERTS=settings.VALIDATE_CERTS == "True",
    MAIL_STARTTLS=settings.MAIL_STARTTLS == "True",
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS == "True",
)


class UserManager(BaseUserManager[User, int]):
    def __init__(self, session: AsyncSession, user_db: BaseUserDatabase[models.UP, models.ID]):
        super().__init__(user_db)
        self.session = session

    def parse_id(self, value: Any) -> int:
        try:
            return int(value)
        except ValueError as e:
            raise InvalidID() from e

    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def authenticate(self, credentials: UserLogin):
        result = await self.session.execute(
            select(User).where(User.email_or_phone == credentials.email_or_phone)
        )
        user = result.scalars().first()
        if not user or not verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )
        return user


#     async def on_after_register(self, user: User, request: Optional[Request] = None):
#         print(f"User {user.id} has registered.")
#
#         message = MessageSchema(
#             subject="Регистрация!",
#             recipients=[user.email],
#             body="Вы успешно зарегистрировались.",
#             subtype=MessageType.plain,
#         )
#
#         fm = FastMail(conf)
#         await fm.send_message(message)
#         return {"message": f"Письмо отправлено на {user.email}"}
#
#     async def on_after_forgot_password(
#         self, user: User, token: str, request: Optional[Request] = None
#     ):
#         print(f"User {user.id} has forgot their password. Reset token: {token}")
#
#     async def on_after_request_verify(
#         self, user: User, token: str, request: Optional[Request] = None
#     ):
#         print(f"Verification requested for user {user.id}. Verification token: {token}")
#
#     async def validate_password(
#         self,
#         password: str,
#         user: UserCreate | User,
#     ) -> None:
#         if len(password) < 8:
#             raise InvalidPasswordException(
#                 reason="Password should be at least 8 characters"
#             )
#         if user.email in password:
#             raise InvalidPasswordException(reason="Password should not contain e-mail")
#         return None
#
#     async def on_after_update(
#         self,
#         user: User,
#         update_dict: Dict[str, Any],
#         request: Optional[Request] = None,
#     ):
#         print(f"User {user.id} has been updated with {update_dict}.")
#
#         message = MessageSchema(
#             subject="Смена пароля!",
#             recipients=[user.email],
#             body="Ваш пароль был успешно изменен.",
#             subtype=MessageType.plain,
#         )
#
#         fm = FastMail(conf)
#         await fm.send_message(message)
#         return {"message": f"Письмо отправлено на {user.email}"}
#
#

async def get_user_manager(session: AsyncSession = Depends(get_session), user_db=Depends(get_user_db)):
    yield UserManager(session, user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
