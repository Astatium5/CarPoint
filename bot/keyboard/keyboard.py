from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choice_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                                   keyboard=[
                                                       [KeyboardButton(text="Получить предложение"), KeyboardButton(
                                                           text="Для инвесторов")],
                                                       [KeyboardButton(text="Контакты"), KeyboardButton(
                                                           text="О проекте"), KeyboardButton(text="Для дистрибьюторов")],
                                                       [KeyboardButton(
                                                           text="Как мы работаем")]
                                                   ])