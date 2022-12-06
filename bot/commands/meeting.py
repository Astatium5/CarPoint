import re
from typing import Any

from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp
from objects import globals
from states.states import Meeting
from utils.api.requests import Requests
from keyboard.keyboard import *
from . import receive_offer
from . import start

api_requests: Requests = Requests()


@dp.message_handler(state=Meeting.name)
async def get_name(message: Message):
    name: str = re.sub("[^a-zA-Zа-яА-Я]", "", message.text)
    response: dict = api_requests.set_name(user_id=message.from_user.id, name=name)

    welcome_page: Any = globals.root.find("welcome")
    await message.answer(welcome_page.find("is_not_city").text)
    return await Meeting.city.set()


@dp.message_handler(state=Meeting.city)
async def get_city(message: Message, state: FSMContext) -> Message:
    city: str = re.sub("[^а-яА-Я]", "", message.text)
    welcome_page: Any = globals.root.find("welcome")

    if not city:
        return await message.answer(welcome_page.find("city_is_not_found").text)
    else:
        response: dict = api_requests.set_city(
            user_id=message.from_user.id, city=city)

        if not response.get("response"):
            return await message.answer(welcome_page.find("city_is_not_found").text)
        else:
            await state.finish()
            await message.answer(response.get("message"))
            return await message.answer(welcome_page.find("is_city").text)
