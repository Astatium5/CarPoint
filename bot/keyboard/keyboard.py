from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton)

from utils.paginate import paginate

choice_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                                   keyboard=[
                                                       [KeyboardButton(text="Получить предложение"), KeyboardButton(
                                                           text="Для инвесторов")],
                                                       [KeyboardButton(text="Контакты"), KeyboardButton(
                                                           text="О проекте"), KeyboardButton(text="Для дистрибьюторов")],
                                                       [KeyboardButton(
                                                           text="Как мы работаем")]
                                                   ])


def marks_markup(marks: list, callback_data: str):
    inline_marks: list = []
    marks: list[list] = list(paginate(marks, 2))
    for mark in marks:
        inline_marks.append([InlineKeyboardButton(
            text=m, callback_data=F"{callback_data}{m}") for m in mark])
    markup = InlineKeyboardMarkup(inline_keyboard=inline_marks)
    return markup