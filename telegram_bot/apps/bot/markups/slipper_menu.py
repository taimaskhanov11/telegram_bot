from telegram_bot.apps.bot.markups.utils import get_inline_keyboard


def cheap_slipper():
    keyboard = [
        (("Да", "yes"),),
        (("Нет", "no"),),
        (("Пересчитать", "recalculate"),),
    ]
    return get_inline_keyboard(keyboard)
def done():
    keyboard = [
        (("Главное меню", "start"),),
        (("Пересчитать", "go"),),
    ]
    return get_inline_keyboard(keyboard)
