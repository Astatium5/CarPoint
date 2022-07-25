from aiogram.types import Message

from objects.globals import dp
from objects import globals

@dp.message_handler(lambda message: message.text == "О проекте")
async def about(message: Message):
    about_page = globals.root.find("about")
    return await message.answer(about_page.text)
