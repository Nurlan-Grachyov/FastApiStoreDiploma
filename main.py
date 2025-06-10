from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.database import create_db_and_tables
from users.routers import log_users_router, register_user, users_router


@asynccontextmanager
async def lifespan(app1: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

log_users_router(app)

register_user(app)

users_router(app)