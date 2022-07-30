import re

from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.storage import FSMContext

from objects import globals
from objects.globals import dp, bot
from states.states import LeaveRequest, LeaveRequestMetaData
from .start import start
from config.config import Config


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
async def get_email(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    email = message.text
    globals.leave_request_metadata.email = email
    await message.answer(leave_request_page.find("input_full_name").text)
    return await LeaveRequest.full_name.set()


@dp.message_handler(state=LeaveRequest.full_name)
async def get_full_name(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    full_name = message.text
    globals.leave_request_metadata.full_name = full_name
    await message.answer(leave_request_page.find("input_address").text)
    return await LeaveRequest.address.set()


@dp.message_handler(state=LeaveRequest.address)
async def get_address(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    address = message.text
    globals.leave_request_metadata.address = address
    _ = globals.leave_request_metadata
    new_leave_request_page = (F"<b>Новая заявка!</b>\n"
                              F"ID пользователя: {message.from_user.id}\n"
                              F"ID автомобиля: {_.car_id}\n"
                              F"Эл. почта: {_.email}\n"
                              F"Полное имя: {_.full_name}\n"
                              F"Адрес: {_.address}\n"
                              F"Подробная информация об автомобиле: <code>http://{config.host}/admin/core/car/{_.car_id}/change</code>")
    await bot.send_message(config.chat_id, new_leave_request_page)
    return await message.answer(leave_request_page.find("end").text)
