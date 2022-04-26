from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from telegram_bot.apps.bot import markups
from telegram_bot.apps.bot.utils.calculate import calculate_mint_slipper_profit


class Mint(StatesGroup):
    sum1 = State()


async def mint_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Введите сумму продажи тапка с минтом в SOL:", reply_markup=types.ReplyKeyboardRemove())
    await Mint.sum1.set()

async def sum_mint(message: types.Message, state: FSMContext):
    mint_sum_number = message.text
    if mint_sum_number.isdigit():
        gst_usdt, sol_usdt, gmt_usdt, gst_sol, money = await calculate_mint_slipper_profit(mint_sum_number)
        await message.answer(f"Твой profit 💰:\n"
                             f"{money} USDT\n"
                             f"{money / gst_usdt} GST\n"
                             f"{money / sol_usdt} SOL\n"
                             f"————————————-\n"
                             f"Курс GTS - {gst_usdt} USDT\n"
                             f"Курс SOL - {sol_usdt} USDT\n"
                             f"Курс GMT - {gmt_usdt} USDT\n"
                             f"Курс -SOL\GST - {gst_sol}")

        await message.answer("81CzVw7QcjrvkUUvb6rnxsTkUJji7B5bUZTFnsEnproJ", reply_markup=markups.slipper_menu.done())
        await state.finish()
    else:
        await message.answer("Пожалуйста введите число")


def register_mint_handlers(dp: Dispatcher):
    callback = dp.register_callback_query_handler
    message = dp.register_message_handler
    callback(mint_start, text="no")
    message(sum_mint, state=Mint.sum1)
