from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from telegram_bot.apps.bot import markups
from telegram_bot.apps.bot.filters.base_filters import UserFilter
from telegram_bot.config.config import config
from telegram_bot.db.models import User


async def start(message: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.finish()
    await message.answer(config.answer.start_message, 'markdown')
    await message.answer("81CzVw7QcjrvkUUvb6rnxsTkUJji7B5bUZTFnsEnproJ", reply_markup=markups.common_menu.start_menu())


async def go(message: types.Message | types.CallbackQuery, user: User, state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.finish()
    await user.use_update()
    await message.answer("Если у тебя выпал хороший тапок ты можешь дополнительно заработать. Хочешь?",
                         reply_markup=markups.common_menu.go())


def register_common_handlers(dp: Dispatcher):
    callback = dp.register_callback_query_handler
    message = dp.register_message_handler
    message(start, UserFilter(), commands="start", state="*")
    callback(start, UserFilter(), text="start", state="*")
    message(go, UserFilter(), commands="recalculate", state="*")
    callback(go, UserFilter(), text="go", state="*")
