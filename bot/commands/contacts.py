from aiogram.types import Message

from objects.globals import dp, bot
from objects import globals

@dp.message_handler(lambda message: message.text == "Контакты")
async def for_investors(message: Message):
    page = globals.root.find("contacts")
    return await message.answer(page.text)
