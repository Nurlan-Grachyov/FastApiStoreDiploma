from alembic.config import Config
from alembic import command
from config.settings import DATABASE_URL
import asyncio


async def main_sync():
    # Создаем конфигурацию Alembic
    alembic_cfg = Config("alembic.ini")

    # Устанавливаем строку подключения динамически из переменной окружения
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)

    # Запускаем миграции (обновление до последней версии)
    command.upgrade(alembic_cfg, "head")

async def main():
    await main_sync()

if __name__ == "__main__":
    asyncio.run(main())