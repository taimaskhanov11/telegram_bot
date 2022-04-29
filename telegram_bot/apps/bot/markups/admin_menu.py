from telegram_bot.apps.bot.markups.utils import get_inline_keyboard


def admin_start():
    keyword = [
        (("👥 Узнать количество пользователей.", "users_count"),),
        (("📄 Узнать процент возврата за сегодня.", "return_percent"),),
        (("✍ Сделать выборку регистраций.", "make_selection"),),
        (("🔖 Сделать рассылку", "send_mail"),),
        (("📋 Стартовое сообщение", "start_message"),),
        (("Изменить COL_GTS", "edit_COL_GTS"),),
        (("Изменить COL_GMT", "edit_COL_GMT"),),
    ]

    return get_inline_keyboard(keyword)


def admin_button():
    keyboard = [
        (("Админ панель", "admin"),),
    ]
    return get_inline_keyboard(keyboard)

def start_message():
    keyboard = [
        (("Изменить", "edit_start_message"),),
    ]
    return get_inline_keyboard(keyboard)
