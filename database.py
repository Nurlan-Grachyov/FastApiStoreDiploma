from tortoise.contrib.fastapi import register_tortoise

from models import app
from settings import DATABASE_URL

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["__main__"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
