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


from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API with JWT",
        version="1.0.0",
        description="JWT auth in Swagger UI",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(lifespan=lifespan)
app.openapi = custom_openapi

app.include_router(user_router)
app.include_router(products_router)

register_user(app)

users_router(app)
