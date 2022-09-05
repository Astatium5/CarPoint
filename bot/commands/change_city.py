from typing import Any

from aiogram.types import Message

from objects.globals import dp
from objects import globals
from states.states import Meeting


@dp.message_handler(lambda message: message.text == "Сменить город")
async def change_city(message: Message):
    welcome_page: Any = globals.root.find("welcome")
    await message.answer(welcome_page.find("is_not_city").text)
    return await Meeting.city.set()