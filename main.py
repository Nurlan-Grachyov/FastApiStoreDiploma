from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth import hash_password, auth_backend, get_user_manager
from database import create_db_and_tables

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from users.models import User
from users.schemas import UserCreate


@asynccontextmanager
async def lifespan(app1: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/register/", response_model=UserCreate)
async def register(user_in: UserCreate, session: AsyncSession = Depends(get_session)):
    if user_in.password != user_in.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    print("match passwords")
    result = await session.execute(
        select(User).where(User.email_or_phone == user_in.email_or_phone)
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email or phone already exists.")
    print("there is not user")
    hashed_password = hash_password(user_in.password)

    new_user = User(
        username=user_in.username,
        email_or_phone=user_in.email_or_phone,
        password=hashed_password,
    )
    print("create user")
    session.add(new_user)
    print("session")
    await session.commit()  # MISTAKE
    print("session commit")
    await session.refresh(new_user)
    print(new_user)
    return new_user


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
