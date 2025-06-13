from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.database import create_db_and_tables
from users.auth import router
from users.routers import register_user, users_router


@asynccontextmanager
async def lifespan(app1: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

register_user(app)

users_router(app)
