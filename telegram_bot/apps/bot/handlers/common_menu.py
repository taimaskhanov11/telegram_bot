from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from telegram_bot.apps.bot import markups
from telegram_bot.apps.bot.filters.base_filters import UserFilter
from telegram_bot.db.models import User


async def start(message: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.finish()
    await message.answer("Hi, Френд 🤞 Выгодно ли минтить?\n\nЭтот вопрос звучит во всех чатах постоянно.\n"
                         "Есть решение, забирай.\nБотМинта Stepn🤖\n\n"
                         "❗️Подходит для расчета продажи тапка только до 2 минтов включительно❗️\n"
                         "❗️10 GMT в расчет добавил\n❗"
                         "Если постоянно минтишь и продаешь 👟, ты все время ищете курс на бирже, считаешь на калькуляторе что бы не уйти в минус, знакомо?\n"
                         "Это Бот для вас. \n"
                         "Экономит уйму времени.\n"
                         "------------------------------------\n"
                         "Делал для себя, пользуйтесь🥷\n"
                         "-------------------------------------\n\n"
                         "Надеюсь при минте тебе выпал достойный тапок ты можешь дополнительно заработать.\n\n"
                         "🏃‍♀️Что сделать\n\n:"
                         "1. Нажать ДА\n"
                         "2. Сначала мы продаем его что бы не потерять энергию 🔋(вводим сумму продажи)\n"
                         "3. Покупаем с рынка с 0 минтом (вводим сумму покупки)\n"
                         "4. Продаем папу хорошего (вводим сумму продажи)\n"
                         "---------------------------------------------\n\n"
                         "🏃‍♂️Что получишь\n\n:"
                         "1. Бот ответит какую доп. прибыль ты получишь в usdt/gst/sol\n"
                         "2. Общий PROFIT🤑\n"
                         "3. Курс монет (в момент запроса данные берутся с биржы)\n"
                         "4. Комиссия маркета в расчетах учтена\n\n"
                         "Цикл сделки:\n"
                         "продажа хорошего тапка с 0 минтом - покупка (дешевого) - продажа папы\n"
                         "-------------------------------------------\n\n"
                         "Если тебе выпал тапок по флору\n\n"
                         "🏃‍♀️Что сделать:\n\n"
                         "1. Нажать НЕТ\n"
                         "2. Продать заминтченого «Папу» \n"
                         "------------------------------------\n\n"
                         "🏃‍♂️Что получишь:\n\n"
                         "1. Твой PROFIT🤑\n"
                         "2. Курс монет (в момент запроса данные берутся с биржы)\n"
                         "3. Комиссия маркета в расчетах учтена\n\n"
                         "---------------------------------\n"
                         "❗️Формат ввода.\n "
                         "Пример: 10.6 - только через точку❗\n️"
                         "-------------------------------------\n"
                         "Курс SOL и GST обновляется автоматически, когда ты обращаешься к боту.\n"
                         "---------------------------------\n"
                         "За подборам тапка , стратегией и пожеланий гоу ко мне @Roman3217 \n"
                         "---------------------------------\n"
                         "Я трачу монетку на поддержание бота, благодарочка за сатошечку.\n"
                         "Много не надо🦌\n"
                         "---------------------------------\n"
                         "Wallet: USDC/GST/SOL👇")
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
