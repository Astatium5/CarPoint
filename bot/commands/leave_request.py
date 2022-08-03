import re

from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import ChatNotFound
from aiogram.dispatcher.storage import FSMContext

from objects import globals
from objects.globals import dp, bot
from states.states import LeaveRequest, LeaveRequestMetaData
from config.config import Config
from log.logger import logger
from . import receive_offer

config = Config()

# Init new LeaveRequestMetaData obj
globals.leave_request_metadata: LeaveRequestMetaData = LeaveRequestMetaData()
# Get receive_offer tag from xml data.
leave_request_page = globals.root.find("leave_request")


@dp.callback_query_handler(lambda query: query.data.startswith(("leave_request#")))
async def leave_request(query: CallbackQuery):
    car_id = re.sub("leave_request#", "", query.data)
    car_id = int(car_id)
    globals.leave_request_metadata.car_id = car_id
    await query.message.answer(leave_request_page.find("input_email").text)
    return await LeaveRequest.email.set()


@dp.message_handler(state=LeaveRequest.email)
async def get_email(message: Message):
    email = message.text
    globals.leave_request_metadata.email = email
    await message.answer(leave_request_page.find("input_full_name").text)
    return await LeaveRequest.full_name.set()


@dp.message_handler(state=LeaveRequest.full_name)
async def get_full_name(message: Message):
    full_name = message.text
    globals.leave_request_metadata.full_name = full_name
    await message.answer(leave_request_page.find("input_address").text)
    return await LeaveRequest.address.set()


@dp.message_handler(state=LeaveRequest.address)
async def get_address(message: Message):
    address = message.text
    globals.leave_request_metadata.address = address
    await message.answer(leave_request_page.find("input_phone").text)
    return await LeaveRequest.phone.set()


@dp.message_handler(state=LeaveRequest.phone)
async def get_phone(message: Message, state: FSMContext):
    phone = re.sub("[^0-9]", "", message.text)
    globals.leave_request_metadata.phone = phone
    _ = globals.leave_request_metadata
    new_leave_request_page = (F"<b>Новая заявка!</b>\n"
                              F"ID пользователя: <code>{message.from_user.id}</code>\n"
                              F"ID автомобиля: <code>{_.car_id}</code>\n"
                              F"Эл. почта: <code>{_.email}</code>\n"
                              F"Полное имя: <code>{_.full_name}</code>\n"
                              F"Адрес: <code>{_.address}</code>\n"
                              F"Номер телефона: <code>{_.phone}</code>\n"
                              F"Подробная информация об автомобиле: <code>http://{config.host}/admin/core/car/{_.car_id}/change</code>")
    try:
        await bot.send_message(config.chat_id, new_leave_request_page)
    except ChatNotFound as e:
        logger.error(e)
    await state.finish()
    return await message.answer(leave_request_page.find("end").text)
