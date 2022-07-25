from aiogram.types import Message

from objects.globals import dp
from objects import globals

@dp.message_handler(lambda message: message.text == "Для дистрибьюторов")
async def for_investors(message: Message):
    page = globals.root.find("for_distributors")
    return await message.answer(page.text)
