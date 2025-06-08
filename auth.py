from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from models import User
from settings import ALGORITHM, SECRET_KEY, pwd_context

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def hash_password(password: str):
    """Хеширует пароль"""
    return pwd_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str):
    """Проверяет пароль"""
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email_or_phone: str, password: str):
    """Проверяет существование пользователя и возвращает объект пользователя."""
    user = await User.filter(email_or_phone=email_or_phone).first()
    if not user:
        return False
    if not await verify_password(password, user.password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: timedelta):
    """Создание JWT-токена."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Получаем текущего пользователя из токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = await User.get(username=username)
    if user is None:
        raise credentials_exception
    return user
