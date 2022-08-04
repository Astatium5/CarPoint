from typing import Any

from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp
from objects import globals


@dp.message_handler(lambda message: message.text == "Как мы работаем", state="*")
async def how_work(message: Message, state: FSMContext) -> Message:
    await state.finish()
    page: Any = globals.root.find("how_work")
    return await message.answer(page.text)
