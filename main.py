from contextlib import asynccontextmanager

from fastapi import FastAPI

from dependencies.database import engine
from products.view import products_router
from users.routers import register_user, user_router, users_router


async def init_models():
    from config.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(products_router)

register_user(app)

users_router(app)
