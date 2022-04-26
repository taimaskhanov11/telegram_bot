import asyncio

from loguru import logger
from tortoise import Tortoise


async def init_tortoise(username, password, host, port, db_name):
    logger.debug(f"Инициализация BD {host}")
    data = {
        "db_url": f"postgres://{username}:{password}@{host}:{port}/{db_name}",
        "modules": {"models": ["telegram_bot.db.models"]},
    }
    try:
        await Tortoise.init(**data)
    except Exception as e:
        logger.critical(e)
        await Tortoise.init(
            **data,
            _create_db=True,
        )
    await Tortoise.generate_schemas()
    logger.debug(f"База данных {db_name} инициализирована")


if __name__ == "__main__":
    asyncio.run(init_tortoise())
