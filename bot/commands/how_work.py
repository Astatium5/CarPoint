from aiogram.types import Message

from objects.globals import dp
from objects import globals


@dp.message_handler(lambda message: message.text == "Как мы работаем")
async def how_work(message: Message):
    page = globals.root.find("how_work")
    return await message.answer(page.text)
