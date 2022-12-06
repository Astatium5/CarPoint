from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton)

from utils.paginate import paginate

choice_markup: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text="Получить предложение"),
     KeyboardButton(text="Для инвесторов")],
    [KeyboardButton(text="Контакты"), KeyboardButton(
        text="О проекте"), KeyboardButton(text="Для дистрибьюторов")],
    [KeyboardButton(text="Как мы работаем")],
    # [KeyboardButton(text="Сменить город")]
])

choice_price_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="500 000₽ - 2 000 000₽",
                          callback_data="pr#87506fd2b91be8b7ab7b59d069c42d40")],
    [InlineKeyboardButton(text="2 000 000₽ - 4 000 000₽",
                          callback_data="pr#1ee1876784dfba4421dfbc93272053a8")],
    [InlineKeyboardButton(text="4 000 000₽ - 6 000 000₽",
                          callback_data="pr#af499ea026c3e952d324d7af4cf7aaee")],
    [InlineKeyboardButton(text="более 6 000 000₽",
                          callback_data="pr#2a3225e2decd960cebe8c4de135f59a0")],
    [InlineKeyboardButton(text="Указать диапазон",
                          callback_data="myself_range")],
    [InlineKeyboardButton(text="Подбери под конкретную сумму",
                          callback_data="specific_amount")],
])

support_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Задать вопрос", callback_data="support"
    )]
])

contact_me_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Свяжитесь со мной", callback_data="contact_me"
    )]
])


def marks_markup(marks: list, callback_data: str) -> InlineKeyboardMarkup:
    inline_marks: list = []
    marks: list[list] = list(paginate(marks, 2))
    for mark in marks:
        inline_marks.append([InlineKeyboardButton(
            text=m, callback_data=F"{callback_data}{m}") for m in mark])
    markup = InlineKeyboardMarkup(inline_keyboard=inline_marks)
    return markup
