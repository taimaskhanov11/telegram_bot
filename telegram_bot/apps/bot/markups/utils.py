from typing import Generator

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def get_inline_button(bnt_data):
    return InlineKeyboardButton(text=bnt_data[0], callback_data=bnt_data[1])


def get_inline_keyboard(ikm_data: list[tuple] | Generator):
    inline_keyboard = (map(get_inline_button, btn) for btn in ikm_data)
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# todo 09.04.2022 20:09 taima: things
def get_keyboard(km_data: list[tuple[str]]):
    return ReplyKeyboardMarkup()
