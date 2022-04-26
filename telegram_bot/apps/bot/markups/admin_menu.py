
from telegram_bot.apps.bot.markups.utils import get_inline_keyboard
from telegram_bot.db.models import User


def admin_start():
    keyword = [
        (("👥 Узнать количество пользователей.", "users_count"),),
        (("🔖 Узнать процент возврата за сегодня.", "return_percent"),),
        (("✍ Сделать выборку регистраций.", "make_selection"),),
    ]

    return get_inline_keyboard(keyword)


def admin_button():
    keyboard = [
        (("Админ панель", "admin"),),
    ]
    return get_inline_keyboard(keyboard)
