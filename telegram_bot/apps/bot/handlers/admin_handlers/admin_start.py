from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from telegram_bot.apps.bot import markups
from telegram_bot.config.config import config
from telegram_bot.db.models import User
from telegram_bot.loader import bot


class MakeSelection(StatesGroup):
    from_ = State()
    to = State()


class SendMail(StatesGroup):
    send = State()


class EditStartMessage(StatesGroup):
    edit = State()

class EditCol(StatesGroup):
    COL_GTS = State()
    COL_GMT = State()

async def admin_start(message: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.finish()

    await message.answer("Добро пожаловать в админ панель. Выберите действие.\n"
                         f"COL_GTS: {config.bot.COL_GTS}\n"
                         f"COL_GMT: {config.bot.COL_GMT}\n",
                         reply_markup=markups.admin_menu.admin_start())


async def users_count(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    users_count_num = await User.all().count()
    await call.message.answer(f"В боте зарегистрировано: {users_count_num} 👥",
                              reply_markup=markups.admin_menu.admin_button())


async def start_message(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer(f"Текущее стартовое сообщение:\n{config.answer.start_message}",
                              reply_markup=markups.admin_menu.start_message())


async def edit_start_message(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Введите новое сообщение для стартового меню", reply_markup=types.ReplyKeyboardRemove())
    await EditStartMessage.edit.set()


async def edit_start_message_done(message: types.Message, state: FSMContext):
    config.answer.start_message = message.text
    await message.answer("Стартовое сообщение успешно изменено")
    await state.finish()


async def edit_COL_GTS(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Введите новое значение для COL_GTS", reply_markup=types.ReplyKeyboardRemove())
    await EditCol.COL_GTS.set()


async def edit_COL_GTS_done(message: types.Message, state: FSMContext):
    config.bot.COL_GTS = float(message.text)
    await message.answer("Значение COL_GTS успешно изменено")
    await state.finish()



async def edit_COL_GMT(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Введите новое значение для COL_GMT", reply_markup=types.ReplyKeyboardRemove())
    await EditCol.COL_GMT.set()


async def edit_COL_GMT_done(message: types.Message, state: FSMContext):
    config.bot.COL_GMT = float(message.text)
    await message.answer("Значение COL_GMT успешно изменено")
    await state.finish()



async def make_selection(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Введите C какой даты сделать выборку. Формат ввода '2022,3,14' - год, месяц, день.")
    await MakeSelection.from_.set()


async def from_make_selection(message: types.Message, state: FSMContext):
    await state.update_data(from_=message.text)
    await message.answer("Введите ДО какой даты сделать выборку. Формат ввода '2022,3,14' - год, месяц, день.")
    await MakeSelection.to.set()


async def to_make_selection(message: types.Message, state: FSMContext):
    to = message.text
    data = await state.get_data()
    users_count, date1, date2 = await User.date_users(from_=data["from_"], to=to)
    await message.answer(f"В период с {date1} до {date2} было зарегистрировано - {users_count} 👥")
    await state.finish()


async def return_percent(call: types.CallbackQuery, state: FSMContext):
    today_online = await User.today_online()
    await call.message.answer(f"Процент возврата на сегодня - {today_online} %",
                              reply_markup=markups.admin_menu.admin_button())
    await state.finish()


async def send_mail(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer(f"Введите текст для рассылки всем пользователям",
                              reply_markup=types.ReplyKeyboardRemove())
    await SendMail.send.set()


async def send_mail_done(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Идет отправка")
    users = await User.all()
    for user in users:
        try:
            await bot.send_message(user.user_id, message.text, "markdown")
        except Exception as e:
            logger.warning(e)
    await message.answer(f"Рассылка отправлена {len(users)} пользователям")


def register_admin_handlers(dp: Dispatcher):
    callback = dp.register_callback_query_handler
    message = dp.register_message_handler
    message(admin_start, user_id=config.bot.admins, commands="admin", state="*")
    callback(admin_start, user_id=config.bot.admins, text="admin", state="*")
    callback(start_message, user_id=config.bot.admins, text="start_message", state="*")
    callback(edit_start_message, user_id=config.bot.admins, text="edit_start_message", state="*")
    message(edit_start_message_done, user_id=config.bot.admins, state=EditStartMessage.edit)

    callback(edit_COL_GTS, user_id=config.bot.admins, text="edit_COL_GTS", state="*")
    message(edit_COL_GTS_done, user_id=config.bot.admins, state=EditCol.COL_GTS)

    callback(edit_COL_GMT, user_id=config.bot.admins, text="edit_COL_GMT", state="*")
    message(edit_COL_GMT_done, user_id=config.bot.admins, state=EditCol.COL_GMT)

    callback(users_count, user_id=config.bot.admins, text="users_count", state="*")
    callback(send_mail, user_id=config.bot.admins, text="send_mail", state="*")
    message(send_mail_done, user_id=config.bot.admins, state=SendMail.send)

    callback(make_selection, user_id=config.bot.admins, text="make_selection", state="*")
    message(from_make_selection, user_id=config.bot.admins, state=MakeSelection.from_)
    message(to_make_selection, user_id=config.bot.admins, state=MakeSelection.to)
    callback(return_percent, user_id=config.bot.admins, text="return_percent", state="*")
