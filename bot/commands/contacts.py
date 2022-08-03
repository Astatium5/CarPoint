from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp
from objects import globals


@dp.message_handler(lambda message: message.text == "Контакты", state="*")
async def for_investors(message: Message, state: FSMContext):
    await state.finish()
    page = globals.root.find("contacts")
    return await message.answer(page.text)
