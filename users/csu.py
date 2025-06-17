import asyncio

from config.database import AsyncSessionLocal
from users.auth import password_helper
from users.models import User


async def create_superuser():
    async with AsyncSessionLocal() as session:
        superuser = User(
            email="superuser@mail.com",
            username="admin",
            phone="+79297278180",
            hashed_password=password_helper.hash("12345678"),
            role="superuser",
            is_active=True,
            is_superuser=True,
            is_verified=True,
        )

        session.add(superuser)

        await session.commit()


asyncio.run(create_superuser())
