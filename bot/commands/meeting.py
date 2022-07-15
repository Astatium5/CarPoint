import re

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp, bot
from objects import globals
from states.states import Meeting
from utils.api.requests import Requests
# from .start import start


api_requests = Requests()


@dp.message_handler(state=Meeting.name)
async def get_name(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    name = re.sub("[^a-zA-Zа-яА-Я]", "", message.text)
    api_requests.set_name(user_id=message.from_user.id, name=name)

    welcome_page = globals.root.find("welcome")
    await message.answer(welcome_page.find("is_not_city").text)
    await Meeting.city.set()


@dp.message_handler(state=Meeting.city)
async def get_city(message: Message, state: FSMContext):
    if message.text == "/start":
        #return await start(message, state)
        pass

    city = re.sub("[^а-яА-Я]", "", message.text)
    welcome_page = globals.root.find("welcome")

    if not city:
        await message.answer(welcome_page.find("city_is_not_found").text)
    else:
        response = api_requests.set_city(user_id=message.from_user.id, city=city)

        if not response.get("response"):
            return await message.answer(welcome_page.find("city_is_not_found").text)
        else:
            await message.answer(response.get("message"))
            #return await start(message, state)
            pass
