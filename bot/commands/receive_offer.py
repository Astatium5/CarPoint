from ast import Call
import re

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.storage import FSMContext
from requests import request

from objects.globals import dp, bot
from objects import globals
from utils.api.requests import Requests
from states.states import *
from .start import start
from log.logger import logger


PRICE_RANGE = {
    "87506fd2b91be8b7ab7b59d069c42d40": {
        "from": 500000,
        "to": 2000000
    },

    "1ee1876784dfba4421dfbc93272053a8": {
        "from": 2000000,
        "to": 4000000
    },

    "af499ea026c3e952d324d7af4cf7aaee": {
        "from": 4000000,
        "to": 6000000
    },

    "2a3225e2decd960cebe8c4de135f59a0": {
        "from": 6000000,
        "to": None
    },
} # Keys is ids price range.

reply_price_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="500 000₽ - 2 000 000₽", callback_data="pr#87506fd2b91be8b7ab7b59d069c42d40")],
    [InlineKeyboardButton(text="2 000 000₽ - 4 000 000₽", callback_data="pr#1ee1876784dfba4421dfbc93272053a8")],
    [InlineKeyboardButton(text="4 000 000₽ - 6 000 000₽", callback_data="pr#af499ea026c3e952d324d7af4cf7aaee")],
    [InlineKeyboardButton(text="более 6 000 000₽", callback_data="pr#2a3225e2decd960cebe8c4de135f59a0")],
])

api_requests = Requests() # Init Requests object.
offer_page = globals.root.find("receive_offer") # Get receive_offer tag from xml data.


@dp.message_handler(lambda message: message.text == "Получить предложение")
async def receive_offer(message: Message):
    response = api_requests.check_phone(user_id=message.from_user.id) # Send check user phone request.

    if not response.get("response"):
        await message.answer(offer_page.find("is_not_phone").text)
        return await ReceiveOffer.phone.set()
    else:
        return await message.answer(offer_page.find("select_price").text, reply_markup=reply_price_markup)

@dp.message_handler(state=ReceiveOffer.phone)
async def get_phone(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    phone = re.sub("[^0-9]", "", message.text) # Remove unnecessary characters, leaving only numbers.

    # Check for correct phone.
    if not phone:
        return await message.answer("Неккоректный номер телефона!")
    globals.phone = int(phone)
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data="is_agree")]
        ]
    )

    await state.finish()
    await message.answer(offer_page.find("personal_data").text, reply_markup=reply_markup)

@dp.callback_query_handler(lambda query: query.data.startswith(("is_agree")))
async def is_agree(query: CallbackQuery, state: FSMContext):
    phone = globals.phone
    if not phone:
        return await query.answer("Бот был перезапущен! Нужно заново заполнить номер телефона.")
    response = api_requests.set_phone(user_id=query.from_user.id, phone=phone)
    if response.get("response"):
        logger.info(F"Set phone! ID: {query.from_user.id}")
        return await new_search(query)

@dp.callback_query_handler(lambda query: query.data.startswith(("pr#")))
async def get_price(query: CallbackQuery):
    price_range_id = re.sub("pr#", "", query.data)
    globals.prfp = PRICE_RANGE.get(price_range_id).get("from") # Price range first part.
    globals.prsp = PRICE_RANGE.get(price_range_id).get("to") # Price range second part.

    response = api_requests.get_all_marks()
    all_marks = response.get("all_marks")

    reply_markup = InlineKeyboardMarkup()

    for mark in all_marks:
        reply_markup.add(InlineKeyboardButton(text=mark, callback_data=F"mark#{mark}"))
    reply_markup.add(InlineKeyboardButton(text="Искать по всем маркам", callback_data="mark#any"),
        InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))

    return await query.message.edit_text(offer_page.find("select_mark").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("mark#")))
async def get_mark(query: CallbackQuery):
    response = api_requests.get_all_bodies()
    bodies = response.get("all_bodies")

    reply_markup = InlineKeyboardMarkup()
    for body in bodies:
        reply_markup.add(InlineKeyboardButton(text=body, callback_data="body#{body}"))
    reply_markup.add(InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))

    return await query.message.edit_text(offer_page.find("select_body").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("body#")))
async def get_body(query: CallbackQuery):
    response = api_requests.get_all_fuel_types()
    fuel_types = response.get("all_fuel_types")

    reply_markup = InlineKeyboardMarkup()
    for fuel_type in fuel_types:
        reply_markup.add(InlineKeyboardButton(text=fuel_type, callback_data=F"fuel_type#{fuel_type}"))
    reply_markup.add(InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))

    return await query.message.edit_text(offer_page.find("select_fuel_type").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("fuel_type#")))
async def get_fuel_type(query: CallbackQuery):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="По объему", callback_data="by_volume")],
            [InlineKeyboardButton(text="По мощности", callback_data="by_power")],
        ]
    )
    reply_markup.add(InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))
    return await query.message.edit_text(offer_page.find("select_volume_or_power").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("by_volume")))
async def get_volume(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(offer_page.find("first_volume_part").text)
    await Volume.first_part.set()


@dp.message_handler(state=Volume.first_part)
async def get_first_volume_part(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)
    await message.answer(offer_page.find("second_volume_part").text)
    await Volume.second_part.set()


@dp.message_handler(state=Volume.second_part)
async def get_second_volume_part(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Механика", callback_data="transmission#МКПП")],
        [InlineKeyboardButton(text="Автомат", callback_data="transmission#АКПП")]
    ])
    reply_markup.add(InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))
    return await message.answer(offer_page.find("select_transmission").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data == "new_search")
async def new_search(query: CallbackQuery):
    offer_page = globals.root.find("receive_offer") # Get receive_offer tag from xml data.
    return await query.message.edit_text(offer_page.find("select_price").text, reply_markup=reply_price_markup)