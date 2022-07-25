import hashlib
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from aiogram.dispatcher.storage import FSMContext
from requests import request


from objects.globals import dp, bot
from objects import globals
from utils.api.requests import Requests
from .meeting import *
from states.states import *


api_requests = Requests()


@dp.message_handler(commands="start")
async def start(message: Message, state: FSMContext):
    globals.start = start
    globals.offer_metadata = OfferMetaData() # Init OfferMetaData and set to vatiable
    globals.offer_metadata.UserId = message.from_user.id
    await state.finish()
    response = api_requests.create_user(user_id=message.from_user.id, first_name=message.from_user.first_name,
        username=message.from_user.username) # Create new user

    bot_info = await bot.get_me() # Get bot info
    welcome_page = globals.root.find("welcome")

    if not response.get("response"):
        if not response.get("name"):
            await message.answer(welcome_page.find("is_empty").text.format(bot_info.first_name))
            return await Meeting.name.set()
        elif not response.get("city"):
            await message.answer(welcome_page.find("is_not_city").text)
            return await Meeting.city.set()
        else:
            reply_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                keyboard=[
                    [KeyboardButton(text="Получить предложение"), KeyboardButton(text="Для инвесторов")],
                    [KeyboardButton(text="Контакты"), KeyboardButton(text="О проекте"), KeyboardButton(text="Для дистрибьюторов")]
                ])
            return await message.answer(welcome_page.find("is_not_empty").text.format(bot_info.first_name),
                reply_markup=reply_markup)
    else:
        await message.answer(welcome_page.find("is_empty").text.format(bot_info.first_name))
        return await Meeting.name.set()
