from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp
from objects import globals


@dp.message_handler(lambda message: message.text == "О проекте", state="*")
async def about(message: Message, state: FSMContext):
    await state.finish()
    about_page = globals.root.find("about")
    return await message.answer(about_page.text)
