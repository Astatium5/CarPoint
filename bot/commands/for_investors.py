from aiogram.types import Message

from objects.globals import dp
from objects import globals

@dp.message_handler(lambda message: message.text == "Для инвесторов")
async def for_investors(message: Message):
    page = globals.root.find("for_investors")
    return await message.answer(page.text)
