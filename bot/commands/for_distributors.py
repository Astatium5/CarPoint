from typing import Any

from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp
from objects import globals

@dp.message_handler(lambda message: message.text == 'Для дистрибьюторов', state='*')
async def for_investors(message: Message, state: FSMContext) -> Message:
    await state.finish()
    page: Any = globals.root.find("for_distributors")
    return await message.answer(page.text)
