from typing import Any

from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp
from objects import globals
from keyboard.keyboard import support_markup

@dp.message_handler(lambda message: message.text == "Контакты", state="*")
async def for_investors(message: Message, state: FSMContext) -> Message:
    await state.finish()
    page: Any = globals.root.find("contacts")
    return await message.answer(page.text, reply_markup=support_markup)
