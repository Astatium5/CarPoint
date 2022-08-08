import re
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import ChatNotFound
from aiogram.dispatcher.storage import FSMContext

from objects import globals
from objects.globals import dp, bot
from states.states import LeaveRequest, LeaveRequestMetaData
from config.config import Config
from log.logger import logger
from utils.api.requests import Requests
from . import receive_offer


api_requests: Requests = Requests()  # Init Requests object.
config: Config = Config()

# Init new LeaveRequestMetaData obj
globals.leave_request_metadata: LeaveRequestMetaData = LeaveRequestMetaData()
# Get receive_offer tag from xml data.
leave_request_page: Any = globals.root.find("leave_request")


@dp.callback_query_handler(lambda query: query.data.startswith(("leave_request#")))
async def leave_request(query: CallbackQuery) -> None:
    car_id: str = re.sub("leave_request#", "", query.data)
    car_id: str = int(car_id)
    globals.leave_request_metadata.car_id = car_id
    await query.message.answer(leave_request_page.find("input_email").text)
    return await LeaveRequest.email.set()


@dp.message_handler(state=LeaveRequest.email)
async def get_email(message: Message) -> None:
    _email: str = re.sub("[^@]+@[^@]+\.[^@]+", "", message.text)
    if _email:
        return await message.answer("Почта не является валидной!")
    email = message.text
    globals.leave_request_metadata.email = email
    await message.answer(leave_request_page.find("input_full_name").text)
    return await LeaveRequest.full_name.set()


@dp.message_handler(state=LeaveRequest.full_name)
async def get_full_name(message: Message) -> None:
    full_name: str = message.text
    globals.leave_request_metadata.full_name = full_name
    await message.answer(leave_request_page.find("input_address").text)
    return await LeaveRequest.address.set()


@dp.message_handler(state=LeaveRequest.address)
async def get_address(message: Message) -> None:
    address: str = message.text
    globals.leave_request_metadata.address = address
    await message.answer(leave_request_page.find("input_phone").text)
    return await LeaveRequest.phone.set()


@dp.message_handler(state=LeaveRequest.phone)
async def get_phone(message: Message, state: FSMContext) -> Message:
    phone = re.sub("[^0-9]", "", message.text)
    if not phone:
        return await message.answer("Телефон не является валидным!")
    globals.leave_request_metadata.phone = phone
    _ = globals.leave_request_metadata
    user_id = message.from_user.id
    username = F"@{message.from_user.username}" if message.from_user.username else "Отсутствует"
    _leave_request_page: str = (
        F"<b>Новая заявка!</b>\n"
        F"ID пользователя: <code>{user_id}</code>\n"
        F"Имя пользователя: {username}\n"
        F"ID автомобиля: <code>{_.car_id}</code>\n"
        F"Эл. почта: <code>{_.email}</code>\n"
        F"Полное имя: <code>{_.full_name}</code>\n"
        F"Адрес: <code>{_.address}</code>\n"
        F"Номер телефона: <code>{_.phone}</code>\n"
        F"Подробная информация об автомобиле: <code>http://{config.host}/admin/core/car/{_.car_id}/change</code>"
    )
    await state.finish()
    response: dict = api_requests.create_entry(user_id=user_id, username=username, car_id=_.car_id, email=_.email,
        name=_.full_name, address=_.address, phone=_.phone)
    if not response.get("response"):
        return await message.answer("Такая заявка уже существует!")
    else:
        try:
            await bot.send_message(config.chat_id, _leave_request_page)
        except ChatNotFound as e:
            logger.error(e)
        return await message.answer(leave_request_page.find("end").text)
