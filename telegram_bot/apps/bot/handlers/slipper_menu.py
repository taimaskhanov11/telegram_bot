from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from telegram_bot.apps.bot import markups
from telegram_bot.apps.bot.utils.calculate import calculate_slipper_profit, calculate_mint_profit


class Slipper(StatesGroup):
    dear_slipper = State()
    cheap_slipper = State()
    done = State()
    mint_check = State()


async def slipper_start(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Что бы получить доп. доход и не потерять энергию,"
                              " надо сначала продать твой тапок с 0-м минтом на рынке и купить более дешевый"
                              " так же с 0-м минтом и только потом продать сминтченый тапок.\n"
                              "Бот рассчитает прибыль сам.", reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer("Введи сумму продажи хорошего тапка в SOL.")
    await Slipper.dear_slipper.set()


async def dear_slipper(message: types.Message, state: FSMContext):
    dear_slipper_num = message.text
    if dear_slipper_num.isdigit():
        await state.update_data(dear_slipper_num=dear_slipper_num)
        await message.answer("Введи сумму покупки более дешевого тапка в SOL.")
        await Slipper.cheap_slipper.set()
    else:
        await message.answer("Пожалуйста введите число")


async def cheap_slipper(message: types.Message, state: FSMContext):
    cheap_slipper_num = message.text
    if cheap_slipper_num.isdigit():
        data = await state.get_data()
        dear_slipper_num = data["dear_slipper_num"]
        gst_usdt, sol_usdt, gmt_usdt, gst_sol, usdt_profit, gst_profit, sol_profit, profit = await calculate_slipper_profit(
            int(dear_slipper_num), int(cheap_slipper_num))
        await state.update_data(
            gst_usdt=gst_usdt,
            sol_usdt=sol_usdt,
            gmt_usdt=gmt_usdt,
            gst_sol=gst_sol,
            usdt_profit=usdt_profit,
            gst_profit=gst_profit,
            sol_profit=sol_profit,
            profit=profit
        )
        await message.answer("Твой profit 💰\n"
                             "Доп. заработок только с продажи хорошо-выпавшего тапка.\n"
                             "————————————————————\n"
                             f"{usdt_profit} USDT\n"
                             f"{gst_profit} GST\n"
                             f"{sol_profit} SOL\n\n"
                             "Цикл сделки:\n"
                             "Продажа тапка с 0 минтом - Покупка тапка (взамен)\n"
                             f"————————————-\nКурс GTS - {gst_usdt} USDT\nКурс SOL - {sol_usdt} USDT\nКурс GMT - {gmt_usdt} USDT\nКурс -SOL\GST - {gst_sol}\n\n")
        await message.answer("Будешь продавать сминтчиный тапок?", reply_markup=markups.slipper_menu.cheap_slipper())
        await Slipper.done.set()
    else:
        await message.answer("Пожалуйста введите число")


async def done(call: types.CallbackQuery, state: FSMContext):
    if call.data == "yes":
        await call.message.answer("Введите сумму продажи тапка с минтом в SOL:",
                                  reply_markup=types.ReplyKeyboardRemove())
        await Slipper.mint_check.set()
    elif call.data == "no":
        await call.message.answer(
            'Хорошо, пишите /Перерасчитать (или нажми на кнопку которая снизу) если я вам сново понадоблюсь!\n'
            'Если хочешь прочитать про бота пиши /start\n'
            '---------------------------------\n'
            'Я трачу монетку на поддержания бота, благодарочка за сатошичку.\n'
            'Много не надо🦌\n'
            '---------------------------------\n'
            'Wallet: USDC/GST/SOL👇\n')
        await call.message.answer("81CzVw7QcjrvkUUvb6rnxsTkUJji7B5bUZTFnsEnproJ", reply_markup=markups.slipper_menu.done())

    elif call.data == "recalculate":
        await call.message.answer("Введи сумму продажи хорошего тапка в SOL.")
        await state.finish()
        await Slipper.dear_slipper.set()


async def mint_check(message: types.Message, state: FSMContext):
    mint_sum = message.text
    if mint_sum.isdigit():
        data = await state.get_data()
        money = await calculate_mint_profit(mint_sum, data)

        await message.answer("Твой profit 💰\n"
                             f"{money} USDT\n"
                             f"{money / data['gst_usdt']} GST\n"
                             f"{money / data['sol_usdt']} SOL\n\n"
                             "Цикл сделки:\n"
                             "Продажа тапка с минтом\n"
                             "————————————————————\n"
                             "🤑*Общая прибыль за всю сделку:*🤑\n"
                             f"{(data['profit'] * data['sol_usdt']) + money} USDT\n"
                             f"{((data['profit'] * data['sol_usdt']) / data['gst_usdt']) + (money / data['gst_usdt'])} GST\n"
                             f"{((data['profit'] * data['sol_usdt']) / data['sol_usdt']) + (money / data['sol_usdt'])} SOL\n"
                             f"————————————-\n\nКурс GTS - {data['gst_usdt']} USDT\n"
                             f"Курс SOL - {data['sol_usdt']} USDT\n"
                             f"Курс GMT - {data['gmt_usdt']} USDT\n"
                             f"Курс -SOL\GST - {data['gst_sol']}\n\n"
                             "Цикл сделки:\n"
                             "Продажа выпавшего тапка с 0 минтом - Покупка тапка (взамен) - Продажа тапка с минтом\n", "markdown")
        await message.answer(
            'Хорошо, пишите /Перерасчитать (или нажми на кнопку которая снизу) если я вам сново понадоблюсь!\n'
            'Если хочешь прочитать про бота пиши /start\n'
            '---------------------------------\n'
            'Я трачу монетку на поддержания бота, благодарочка за сатошичку.\n'
            'Много не надо🦌\n'
            '---------------------------------\n'
            'Wallet: USDC/GST/SOL👇', )
        await message.answer("81CzVw7QcjrvkUUvb6rnxsTkUJji7B5bUZTFnsEnproJ", reply_markup=markups.slipper_menu.done())

    else:
        await message.answer("Пожалуйста введите число")


def register_slipper_handlers(dp: Dispatcher):
    callback = dp.register_callback_query_handler
    message = dp.register_message_handler
    callback(slipper_start, text="yes")
    message(dear_slipper, state=Slipper.dear_slipper)
    message(cheap_slipper, state=Slipper.cheap_slipper)
    callback(done, state=Slipper.done)
    message(mint_check, state=Slipper.mint_check)
