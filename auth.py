from fastapi_mail import ConnectionConfig, MessageSchema, FastMail, MessageType
from typing import Optional, Any, Dict
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from fastapi import Request
from fastapi_users import BaseUserManager, InvalidID, InvalidPasswordException
from fastapi_users_db_tortoise import TortoiseUserDatabase

import settings
from models import User
from schemas import UserCreate
from settings import SECRET_KEY

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

conf = ConnectionConfig(MAIL_USERNAME=settings.MAIL_USERNAME,
                        MAIL_PASSWORD=settings.MAIL_PASSWORD,
                        MAIL_FROM=settings.MAIL_FROM,
                        MAIL_PORT=settings.MAIL_PORT,
                        MAIL_SERVER=settings.MAIL_SERVER,
                        USE_CREDENTIALS=settings.USE_CREDENTIALS == 'True',
                        VALIDATE_CERTS=settings.VALIDATE_CERTS == 'True',
                        MAIL_STARTTLS=settings.MAIL_STARTTLS == 'True',
                        MAIL_SSL_TLS=settings.MAIL_SSL_TLS == 'True')


class UserManager(BaseUserManager[User, int]):
    def parse_id(self, value: Any) -> int:
        try:
            return int(value)
        except ValueError as e:
            raise InvalidID() from e

    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

        message = MessageSchema(
            subject="Регистрация!",
            recipients=[user.email],
            body="Вы успешно зарегистрировались.",
            subtype=MessageType.plain
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        return {"message": f"Письмо отправлено на {user.email}"}

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def validate_password(
            self,
            password: str,
            user: UserCreate | User,
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )
        return None

    async def on_after_update(
            self,
            user: User,
            update_dict: Dict[str, Any],
            request: Optional[Request] = None,
    ):
        print(f"User {user.id} has been updated with {update_dict}.")

        message = MessageSchema(
            subject="Смена пароля!",
            recipients=[user.email],
            body="Ваш пароль был успешно изменен.",
            subtype=MessageType.plain
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        return {"message": f"Письмо отправлено на {user.email}"}


user_db_adapter = TortoiseUserDatabase(User, User)


async def get_user_manager(user_db=user_db_adapter):
    yield UserManager(user_db)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)