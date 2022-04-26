from telegram_bot.apps.bot.markups.utils import get_inline_keyboard


def start_menu():
    keyboard = [
        (("GO", "go"),),
    ]
    return get_inline_keyboard(keyboard)

def go():
    keyboard = [
        (("Да", "yes"),),
        (("Нет", "no"),),
    ]
    return get_inline_keyboard(keyboard)




def menu_button():
    keyboard = [
        (("Главное меню", "start"),),
    ]
    return get_inline_keyboard(keyboard)


def choice():
    keyboard = [
        (("Да", "yes"),),
        (("Нет", "no"),),
    ]
    return get_inline_keyboard(keyboard)
