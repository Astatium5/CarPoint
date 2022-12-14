from typing import Union, Any

from aiogram.types import Message

from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp, bot
from objects import globals
from utils.api.requests import Requests
from .meeting import *
from states.states import *
from keyboard.keyboard import choice_markup

api_requests: Requests = Requests()

@dp.message_handler(commands="start", state="*")
async def start(message: Message, state: FSMContext) -> Union[Message, None]:
    if message.chat.type != "group":
        globals.start = start
        # Init OfferMetaData and set to variable
        globals.offer_metadata = OfferMetaData()
        await state.finish()
        response: dict = api_requests.create_user(user_id=message.from_user.id, first_name=message.from_user.first_name,
                                                  username=message.from_user.username)  # Create new user

        if response:
            bot_info = await bot.get_me()  # Get bot info
            welcome_page: Any = globals.root.find("welcome")

            if not response.get("response"):
                if not response.get("name"):
                    await message.answer(welcome_page.find("is_empty").text.format(bot_info.first_name))
                    return await Meeting.name.set()
                elif not response.get("city"):
                    await message.answer(welcome_page.find("is_not_city").text)
                    return await Meeting.city.set()
                else:
                    return await message.answer(welcome_page.find("is_not_empty").text.format(bot_info.first_name),
                                                reply_markup=choice_markup)
            else:
                await message.answer(welcome_page.find("is_empty").text.format(bot_info.first_name))
            return await Meeting.name.set()
