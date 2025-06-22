import asyncio
import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import command, context
from users.models import Base

load_dotenv()
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# target_metadata = mymodel.Base.metadata

# get database URL from environment
database_url = os.getenv("DATABASE_URL")
config.set_main_option("sqlalchemy.url", database_url)


async def run_migrations_online():
    connect_args = {}
    connect_args["server_settings"] = {"async_mode": "aiohttp"}
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )

    async with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            dialect_opts={"paramstyle": "pyformat"},
        )

        with context.begin_transaction():
            command.upgrade(connection, "head")


if __name__ == "__main__":
    asyncio.run(run_migrations_online())
