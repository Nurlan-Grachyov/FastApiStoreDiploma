from tortoise.contrib.fastapi import register_tortoise

from models import app

register_tortoise(
    app,
    db_url='postgres://postgres:12345678@localhost:5432/StoreDiploma',
    modules={'models': ['__main__']},
    generate_schemas=True,
    add_exception_handlers=True,
)