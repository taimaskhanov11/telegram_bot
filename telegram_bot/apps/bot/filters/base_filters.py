from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from telegram_bot.config.config import config
from telegram_bot.db.models import User


class UserFilter(BoundFilter):
    async def check(self, call: types.CallbackQuery, *args, **kwargs):
        logger.trace(f"{call=}")
        user = call.from_user
        user, _is_created = await User.get_or_create(
            user_id=user.id,
            defaults={
                "username": user.username,
                "language": user.language_code,
            },
        )
        if _is_created:
            logger.info(f"Новый пользователь {user=}")
        if user.user_id in config.bot.block_list:
            logger.warning(f"{user.user_id} заблокирован")
            return False
        return {"user": user}
