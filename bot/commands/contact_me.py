import re
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import ChatNotFound

from objects.globals import *
from objects import globals
from config.config import Config
from states.states import *
from log.logger import logger
from . import receive_offer

config: Config = Config()
contact_me_page: Any = globals.root.find("contact_me")

@dp.callback_query_handler(lambda query: query.data == "contact_me")
async def contact_me(query: CallbackQuery):
    await query.message.answer(contact_me_page.find("name").text)
    return await ContactMe.name.set()


@dp.message_handler(state=ContactMe.name)
async def get_name(message: Message):
    name: str = message.text
    globals.ContactMeMetaData.name = name
    await message.answer(contact_me_page.find("email").text)
    return await ContactMe.email.set()


@dp.message_handler(state=ContactMe.email)
async def get_email(message: Message):
    _email: str = re.sub("[^@]+@[^@]+\.[^@]+", "", message.text)
    if _email:
        return await message.answer("Почта не является валидной!")
    email: str = message.text
    globals.ContactMeMetaData.email = email
    await message.answer(contact_me_page.find("phone").text)
    return await ContactMe.phone.set()


@dp.message_handler(state=ContactMe.phone)
async def get_phone(message: Message, state: FSMContext):
    phone: str = re.sub("[^0-9]", "", message.text)
    if not phone:
        return await message.answer("Телефон не является валидным!")
    globals.ContactMeMetaData.phone = phone

    _ = globals.ContactMeMetaData
    user_id: int = message.from_user.id
    username: str = F"@{message.from_user.username}" if message.from_user.username else "Отсутствует"
    _contact_me_page: str = (
        F"<b>Связь с инвестором!</b>\n"
        F"ID пользователя:  <code>{user_id}</code>\n"
        F"Имя пользователя: {username}\n"
        F"Имя: <code>{_.name}</code>\n"
        F"Почта: <code>{_.email}</code>\n"
        F"Телефон: <code>{_.phone}</code>"
    )
    try:
        await bot.send_message(config.chat_id, _contact_me_page)
    except ChatNotFound as e:
        logger.error(e)
    await state.finish()
    return await message.answer(contact_me_page.find("end").text)
