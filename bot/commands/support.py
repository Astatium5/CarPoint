import re
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import ChatNotFound

from objects.globals import dp, bot
from objects import globals
from config.config import Config
from states.states import Support
from log.logger import logger
from . import receive_offer

config: Config = Config()
support_page: Any = globals.root.find("support")

@dp.callback_query_handler(lambda query: query.data == "support")
async def support(query: CallbackQuery):
    await query.message.answer(support_page.find("name").text)
    return await Support.name.set()


@dp.message_handler(state=Support.name)
async def get_name(message: Message):
    name: str = message.text
    globals.SupportMetaData.name = name
    await message.answer(support_page.find("email").text)
    return await Support.email.set()


@dp.message_handler(state=Support.email)
async def get_email(message: Message):
    _email: str = re.sub(r"[^@]+@[^@]+\.[^@]+", "", message.text)
    if _email:
        return await message.answer("Почта не является валидной!")
    email: str = message.text
    globals.SupportMetaData.email = email
    await message.answer(support_page.find("phone").text)
    return await Support.phone.set()


@dp.message_handler(state=Support.phone)
async def get_phone(message: Message):
    phone: str = re.sub("[^0-9]", "", message.text)
    if not phone:
        return await message.answer("Телефон не является валидным!")
    globals.SupportMetaData.phone = phone
    await message.answer(support_page.find("question").text)
    return await Support.question.set()


@dp.message_handler(state=Support.question)
async def get_question(message: Message, state: FSMContext):
    question: str = message.text
    globals.SupportMetaData.question = question
    _ = globals.SupportMetaData
    user_id: int = message.from_user.id
    username = F"@{message.from_user.username}" if message.from_user.username else "Отсутствует"
    _support_page: str = (
        F"<b>Новый вопрос. (BOT)</b>\n"
        F"ID пользователя: <code>{user_id}</code>\n"
        F"Имя пользователя: {username}\n"
        F"Имя: <code>{_.name}</code>\n"
        F"Почта: <code>{_.email}</code>\n"
        F"Телефон: <code>{_.phone}</code>\n"
        F"Вопрос: <code>{_.question}</code>"
    )
    try:
        await bot.send_message(config.chat_id, _support_page)
    except ChatNotFound as e:
        logger.error(e)
    await state.finish()
    return await message.answer(support_page.find("end").text)
