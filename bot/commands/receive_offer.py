import re

from aiogram.types import (Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.types import (InlineQuery,
    InputTextMessageContent, InlineQueryResultArticle)
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageNotModified, BadRequest

from objects.globals import dp, bot
from objects import globals
from utils.api.requests import Requests
from states.states import *
from .start import start
from log.logger import logger
from utils.converter import *


MAX_SHOW: int = 50

PRICE_RANGE = {
    "87506fd2b91be8b7ab7b59d069c42d40": {
        "min": 500000,
        "max": 2000000
    },

    "1ee1876784dfba4421dfbc93272053a8": {
        "min": 2000000,
        "max": 4000000
    },

    "af499ea026c3e952d324d7af4cf7aaee": {
        "min": 4000000,
        "max": 6000000
    },

    "2a3225e2decd960cebe8c4de135f59a0": {
        "min": 6000000,
        "max": 0
    },
} # Keys is ids price range.

reply_price_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="500 000₽ - 2 000 000₽", callback_data="pr#87506fd2b91be8b7ab7b59d069c42d40")],
    [InlineKeyboardButton(text="2 000 000₽ - 4 000 000₽", callback_data="pr#1ee1876784dfba4421dfbc93272053a8")],
    [InlineKeyboardButton(text="4 000 000₽ - 6 000 000₽", callback_data="pr#af499ea026c3e952d324d7af4cf7aaee")],
    [InlineKeyboardButton(text="более 6 000 000₽", callback_data="pr#2a3225e2decd960cebe8c4de135f59a0")],
    [InlineKeyboardButton(text="Указать диапазон", callback_data="myself_range")],
    [InlineKeyboardButton(text="Подбери под конкретную сумму", callback_data="specific_amount")],
])

api_requests: Requests = Requests() # Init Requests object.
offer_page = globals.root.find("receive_offer") # Get receive_offer tag from xml data.
globals.offer_metadata: OfferMetaData = OfferMetaData() # Init OfferMetaData and set to vatiable


@dp.message_handler(lambda message: message.text == "Получить предложение")
async def receive_offer(message: Message):
    response: dict = api_requests.check_phone(user_id=message.from_user.id) # Send check user phone request.

    if not response.get("response"):
        await message.answer(offer_page.find("is_not_phone").text)
        return await ReceiveOffer.phone.set()
    else:
        globals.offer_metadata = OfferMetaData()
        return await message.answer(offer_page.find("select_price").text, reply_markup=reply_price_markup)


@dp.message_handler(state=ReceiveOffer.phone)
async def get_phone(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    phone: str = re.sub("[^0-9]", "", message.text) # Remove unnecessary characters, leaving only numbers.

    # Check for correct phone.
    if not phone:
        return await message.answer("Некорректный номер телефона!")
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
        return await new_search(query)


@dp.callback_query_handler(lambda query: query.data.startswith(("pr#")))
async def get_price(query: CallbackQuery):
    price_range_id = re.sub("pr#", "", query.data)
    price_range = PRICE_RANGE.get(price_range_id)
    globals.offer_metadata.MinPrice = price_range.get("min")
    globals.offer_metadata.MaxPrice = price_range.get("max")

    response = api_requests.get_all_marks()
    all_marks = response.get("all_marks")

    reply_markup = InlineKeyboardMarkup()

    for mark in all_marks:
        reply_markup.add(InlineKeyboardButton(text=mark, callback_data=F"mark#{mark}"))
    reply_markup.add(
        InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))
    # InlineKeyboardButton(text="Искать по всем маркам", callback_data="mark#any")

    try:
        return await query.message.edit_text(offer_page.find("select_mark").text, reply_markup=reply_markup)
    except MessageNotModified as e:
        logger.error(e)


@dp.callback_query_handler(lambda query: query.data.startswith(("myself_range")))
async def myself_range(query: CallbackQuery):
    await query.message.edit_text(offer_page.find("min_price").text)
    return await Price.min.set()


@dp.message_handler(state=Price.min)
async def get_min_price(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    if not is_int(message.text):
        return await message.answer("Некорректный формат ввода!")
    globals.offer_metadata.MinPrice = message.text
    await message.answer(offer_page.find("max_price").text)
    return await Price.max.set()


@dp.message_handler(state=Price.max)
async def get_max_price(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    if not is_int(message.text):
        return await message.answer("Некорректный формат ввода!")
    await state.finish()
    globals.offer_metadata.MaxPrice = message.text
    response = api_requests.get_all_marks()
    all_marks = response.get("all_marks")

    reply_markup = InlineKeyboardMarkup()

    for mark in all_marks:
        reply_markup.add(InlineKeyboardButton(text=mark, callback_data=F"mark#{mark}"))
    reply_markup.add(InlineKeyboardButton(text="Искать по всем маркам", callback_data="mark#any"),
        InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))
    return await message.answer(offer_page.find("select_mark").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("specific_amount")))
async def specific_amount(query: CallbackQuery):
    await query.message.edit_text(offer_page.find("specific_amount").text)
    return await Price.specific_amount.set()


@dp.message_handler(state=Price.specific_amount)
async def get_specific_amount(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    if not is_int(message.text):
        return await message.answer("Некорректный формат ввода!")
    await state.finish()
    globals.offer_metadata.MinPrice = message.text
    response = api_requests.get_all_marks()
    all_marks = response.get("all_marks")

    reply_markup = InlineKeyboardMarkup()

    for mark in all_marks:
        reply_markup.add(InlineKeyboardButton(text=mark, callback_data=F"mark#{mark}"))
    reply_markup.add(
        InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))
    # InlineKeyboardButton(text="Искать по всем маркам", callback_data="mark#any")

    return await message.answer(offer_page.find("select_mark").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("mark#")))
async def get_mark(query: CallbackQuery):
    mark = re.sub("mark#", "", query.data)
    if mark == "any":
        globals.offer_metadata.IsAnyMark = True
    else:
        globals.offer_metadata.Mark = mark

    response = api_requests.get_all_bodies(mark=mark)
    bodies = response.get("all_bodies")

    reply_markup = InlineKeyboardMarkup()

    if bodies:
        for body in bodies:
            reply_markup.add(InlineKeyboardButton(text=body, callback_data=F"body#{body}"))
        text = offer_page.find("select_body").text
    else:
        text = offer_page.find("not_found").text
    reply_markup.add(InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))

    return await query.message.edit_text(text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("body#")))
async def get_body(query: CallbackQuery):
    body = re.sub("body#", "", query.data)
    globals.offer_metadata.Body = body
    response = api_requests.get_all_fuel_types(mark=globals.offer_metadata.Mark, body=body, user_id=query.from_user.id,
        min_price=globals.offer_metadata.MinPrice, max_price=globals.offer_metadata.MaxPrice)
    fuel_types = response.get("all_fuel_types")

    reply_markup = InlineKeyboardMarkup()

    if fuel_types:
        n = 0
        for fuel_type in fuel_types:
            reply_markup.add(InlineKeyboardButton(text=fuel_type, callback_data=F"fuel_type#{fuel_type}"))
            n+=1
        if n > 1:
            reply_markup.add(InlineKeyboardButton(text="Любой", callback_data="fuel_type#any"))
        text = offer_page.find("select_fuel_type").text
    else:
        text = offer_page.find("not_found").text
    reply_markup.add(InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))

    try:
        return await query.message.edit_text(text, reply_markup=reply_markup)
    except MessageNotModified as e:
        logger.error(e)


@dp.callback_query_handler(lambda query: query.data.startswith(("fuel_type#")))
async def get_fuel_type(query: CallbackQuery):
    fuel_type = re.sub("fuel_type#", "", query.data)
    if fuel_type == "any":
        globals.offer_metadata.IsAnyFuelType = True
    else:
        globals.offer_metadata.FuelType = fuel_type
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
    globals.offer_metadata.IsVolume = True
    await query.message.edit_text(offer_page.find("min_volume").text)
    return await Volume.min.set()


@dp.message_handler(state=Volume.min)
async def get_min_volume(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    if not is_float(message.text):
        return await message.answer("Некорректный формат ввода!")
    globals.offer_metadata.MinVolume = message.text
    await message.answer(offer_page.find("max_volume").text)
    return await Volume.max.set()


@dp.message_handler(state=Volume.max)
async def get_max_volume(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    if not is_float(message.text):
        return await message.answer("Некорректный формат ввода!")
    await state.finish()
    globals.offer_metadata.MaxVolume = message.text
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Механика", switch_inline_query_current_chat="МКПП")],
        [InlineKeyboardButton(text="Автомат", switch_inline_query_current_chat="АКПП")],
    ])
    reply_markup.add(InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))
    return await message.answer(offer_page.find("select_transmission").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("by_power")))
async def get_power(query: CallbackQuery):
    globals.offer_metadata.IsPower = True
    await query.message.edit_text(offer_page.find("min_power").text)
    return await Power.min.set()


@dp.message_handler(state=Power.min)
async def get_min_power(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    if not is_int(message.text):
        return await message.answer("Некорректный формат ввода!")
    globals.offer_metadata.MinPower = message.text
    await message.answer(offer_page.find("max_power").text)
    return await Power.max.set()


@dp.message_handler(state=Power.max)
async def get_max_power(message: Message, state: FSMContext):
    if message.text == "/start":
        return await start(message, state)

    if not is_int(message.text):
        return await message.answer("Некорректный формат ввода!")
    await state.finish()
    globals.offer_metadata.MaxPower = message.text
    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Механика", switch_inline_query_current_chat="МКПП")],
        [InlineKeyboardButton(text="Автомат", switch_inline_query_current_chat="АКПП")],
    ])
    reply_markup.add(InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))
    return await message.answer(offer_page.find("select_transmission").text, reply_markup=reply_markup)


@dp.inline_handler()
async def inline_echo(query: InlineQuery):
    if not globals.offer_metadata.Body:
        return await not_found(query)

    transmission: str = query.query
    globals.offer_metadata.Transmission = transmission
    _ = globals.offer_metadata
    response: dict = api_requests.find_car(body=_.Body, fuel_type=_.FuelType, user_id=query.from_user.id,
        transmission=_.Transmission, **globals.offer_metadata.to_header())

    status = bool(response.get("response"))
    if status:
        cars = response.get("cars")
        if cars:
            n = 0
            items = []
            for car in cars:
                id = car.get("id")
                title = car.get("title")
                price = car.get("price")
                image = car.get("image")
                engine_volume = car.get("engine_volume")
                engine_power = car.get("engine_power")
                type_fuel = car.get("engine_type_fuel")
                wd = car.get("wd")
                item = InlineQueryResultArticle(id=id, title=title,
                    input_message_content=InputTextMessageContent(title),
                    description=(F"Цена: {int(price)}₽\t"
                                 F"Объем: {engine_volume}\t"
                                 F"Мощность: {engine_power}\t"
                                 F"Тип: {type_fuel},\t"
                                 F"{wd}"),
                    hide_url=True, thumb_url=image)
                items.append(item)
                n+=1
                if n == MAX_SHOW:
                    break
            return await globals.bot.answer_inline_query(query.id, items, cache_time=3)
        else:
            return await not_found(query)
    else:
        return await not_found(query)


@dp.callback_query_handler(lambda query: query.data == "new_search")
async def new_search(query: CallbackQuery):
    globals.offer_metadata = OfferMetaData()
    offer_page = globals.root.find("receive_offer") # Get receive_offer tag from xml data.
    try:
        return await query.message.edit_text(offer_page.find("select_price").text, reply_markup=reply_price_markup)
    except BadRequest:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        return await bot.send_message(chat_id=query.message.chat.id, text=offer_page.find("select_price").text, reply_markup=reply_price_markup)


async def not_found(query: InlineQuery):
    thumb = "https://raw.githubusercontent.com/amtp1/CarPoint/main/image/thumb.png"
    not_found_item = InlineQueryResultArticle(
        id=-1, title="Автомобиль не найден!", input_message_content=InputTextMessageContent("Auto not found"),
        description="Нам не удалось найти автомобиль по данным параметрам.", hide_url=True, thumb_url=thumb)
    return await globals.bot.answer_inline_query(query.id, [not_found_item], cache_time=3)
