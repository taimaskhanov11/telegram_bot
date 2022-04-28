import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand
from loguru import logger

from telegram_bot.apps.bot.handlers.admin_handlers.admin_start import register_admin_handlers
from telegram_bot.apps.bot.handlers.common_menu import register_common_handlers
from telegram_bot.apps.bot.handlers.mint_menu import register_mint_handlers
from telegram_bot.apps.bot.handlers.slipper_menu import register_slipper_handlers
from telegram_bot.config.config import config, config_file
from telegram_bot.config.setting_logging import init_logging
from telegram_bot.db.db_main import init_tortoise
from telegram_bot.loader import bot, dp


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню"),
        BotCommand(command="/admin", description="Админ меню"),
        BotCommand(command="/recalculate", description="Пересчитать"),
    ]
    await bot.set_my_commands(commands)


# todo 01.04.2022 1:08 taima:  tzlocal, scheduler
# todo 01.04.2022 15:29 taima: F, Q tortoise;atomic;
async def main():
    # Настройка логирования
    init_logging(
        filename=config_file or "",
        old_logger=True,
        level="TRACE",
        # old_level=logging.DEBUG,
        old_level=logging.INFO,
        steaming=True,
        write=True,
    )

    logger.success(f"Starting bot {(await bot.get_me()).username}")

    # Установка команд бота
    await set_commands(bot)

    # Инициализация бд
    await init_tortoise(**config.db.dict())

    # Регистрация хэндлеров
    register_common_handlers(dp)
    register_admin_handlers(dp)
    register_mint_handlers(dp)
    register_slipper_handlers(dp)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.get_event_loop()
