import re
from collections import Counter
from typing import Any, Dict, Union

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
from log.logger import logger
from utils.converter import *
from keyboard.keyboard import *
from . import start

MAX_SHOW: int = 20

PRICE_RANGE: dict = {
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
}  # Keys is ids price range.

api_requests: Requests = Requests()  # Init Requests object.
# Get receive_offer tag from xml data.
offer_page: Any = globals.root.find("receive_offer")
# Init OfferMetaData and set to vatiable
globals.offer_metadata: OfferMetaData = OfferMetaData()


@dp.message_handler(lambda message: message.text == "Получить предложение", state="*")
async def receive_offer(message: Message, state: FSMContext) -> Message:
    await state.finish()
    # Send check user phone request.
    # response: dict = api_requests.check_phone(user_id=message.from_user.id)

    # if not response.get("response"):
    #     await message.answer(offer_page.find("is_not_phone").text)
    #     return await ReceiveOffer.phone.set()
    # else:
    globals.offer_metadata = OfferMetaData()
    return await message.answer(offer_page.find("select_price").text, reply_markup=choice_price_markup)


@dp.message_handler(state=ReceiveOffer.phone)
async def get_phone(message: Message, state: FSMContext) -> Message:
    # Remove unnecessary characters, leaving only numbers.
    phone: str = re.sub("[^0-9]", "", message.text)

    # Check for correct phone.
    if not phone:
        return await message.answer("Некорректный номер телефона!")
    globals.phone: int = int(phone)
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить",
                                  callback_data="is_agree")]
        ]
    )

    await state.finish()
    return await message.answer(offer_page.find("personal_data").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("is_agree")))
async def is_agree(query: CallbackQuery) -> Any:
    phone = globals.phone
    if not phone:
        return await query.answer("Бот был перезапущен! Нужно заново ввести номер телефона.")
    response = api_requests.set_phone(user_id=query.from_user.id, phone=phone)
    if response.get("response"):
        return await new_search(query)


@dp.callback_query_handler(lambda query: query.data.startswith(("pr#")))
async def get_price(query: CallbackQuery) -> Union[Message, None]:
    price_range_id: str = re.sub("pr#", "", query.data)  # Get price range id.
    # Get price range.
    price_range: Dict[str, int] = PRICE_RANGE.get(price_range_id)
    globals.offer_metadata.MinPrice = price_range.get("min")
    globals.offer_metadata.MaxPrice = price_range.get("max")

    response: dict = api_requests.get_all_marks(min_price=globals.offer_metadata.MinPrice, max_price=globals.offer_metadata.MaxPrice)
    all_marks: Union[Any, None] = response.get("all_marks")
    all_marks.sort()

    reply_markup = marks_markup(marks=all_marks, callback_data="mark#")
    reply_markup.add(
        InlineKeyboardButton(text="Искать по всем маркам", callback_data="mark#any"),
        InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))

    try:
        return await query.message.edit_text(offer_page.find("select_mark").text, reply_markup=reply_markup)
    except MessageNotModified as e:
        logger.error(e)


@dp.callback_query_handler(lambda query: query.data.startswith(("myself_range")))
async def myself_range(query: CallbackQuery) -> None:
    await query.message.edit_text(offer_page.find("min_price").text)
    return await Price.min.set()


@dp.message_handler(state=Price.min)
async def get_min_price(message: Message) -> Union[Message, None]:
    if not is_int(message.text):
        return await message.answer("Некорректный формат ввода!")
    globals.offer_metadata.MinPrice = message.text
    await message.answer(offer_page.find("max_price").text)
    return await Price.max.set()


@dp.message_handler(state=Price.max)
async def get_max_price(message: Message, state: FSMContext) -> Message:
    if not is_int(message.text):
        return await message.answer("Некорректный формат ввода!")
    await state.finish()
    globals.offer_metadata.MaxPrice = message.text
    response: dict = api_requests.get_all_marks(min_price=globals.offer_metadata.MinPrice, max_price=globals.offer_metadata.MaxPrice)
    all_marks: Union[Any, None] = response.get("all_marks")
    all_marks.sort()

    reply_markup = marks_markup(marks=all_marks, callback_data="mark#")
    reply_markup.add(
        InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))
    return await message.answer(offer_page.find("select_mark").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("specific_amount")))
async def specific_amount(query: CallbackQuery) -> None:
    await query.message.edit_text(offer_page.find("specific_amount").text)
    return await Price.specific_amount.set()


@dp.message_handler(state=Price.specific_amount)
async def get_specific_amount(message: Message, state: FSMContext) -> Message:
    if not is_int(message.text):
        return await message.answer("Некорректный формат ввода!")
    await state.finish()
    globals.offer_metadata.MinPrice = message.text
    response: dict = api_requests.get_all_marks(min_price=globals.offer_metadata.MinPrice, max_price=globals.offer_metadata.MaxPrice)
    all_marks: Union[Any, None] = response.get("all_marks")
    all_marks.sort()

    reply_markup = marks_markup(marks=all_marks, callback_data="mark#")
    reply_markup.add(
        InlineKeyboardButton(text="Начать поиск сначала", callback_data="new_search"))

    return await message.answer(offer_page.find("select_mark").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("mark#")))
async def get_mark(query: CallbackQuery) -> Union[Message, None]:
    mark: str = re.sub("mark#", "", query.data)
    if mark == "any":
        globals.offer_metadata.IsAnyMark = True
    else:
        globals.offer_metadata.Mark = mark

    response: dict = api_requests.get_all_bodies(mark=mark,
        min_price=globals.offer_metadata.MinPrice, max_price=globals.offer_metadata.MaxPrice)
    bodies: Union[Any, None] = response.get("all_bodies")

    reply_markup = InlineKeyboardMarkup()

    if bodies:
        for body in bodies:
            reply_markup.add(InlineKeyboardButton(
                text=body, callback_data=F"body#{body}"))
        text: Any = offer_page.find("select_body").text
    else:
        text: Any = offer_page.find("not_found").text
    reply_markup.add(InlineKeyboardButton(
        text="Начать поиск сначала", callback_data="new_search"))

    try:
        return await query.message.edit_text(text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(e)


@dp.callback_query_handler(lambda query: query.data.startswith(("body#")))
async def get_body(query: CallbackQuery):
    body: str = re.sub("body#", "", query.data)
    mark = globals.offer_metadata.Mark
    globals.offer_metadata.Body = body
    response: dict = api_requests.get_all_fuel_types(mark=mark if mark else "any", body=body,
                                                     min_price=globals.offer_metadata.MinPrice, max_price=globals.offer_metadata.MaxPrice)
    fuel_types = response.get("all_fuel_types")

    reply_markup = InlineKeyboardMarkup()

    if fuel_types:
        n: int = 0
        for fuel_type in fuel_types:
            reply_markup.add(InlineKeyboardButton(
                text=fuel_type, callback_data=F"fuel_type#{fuel_type}"))
            n += 1
        if n > 1:
            reply_markup.add(InlineKeyboardButton(
                text="Любой", callback_data="fuel_type#any"))
        text: Any = offer_page.find("select_fuel_type").text
    else:
        text: Any = offer_page.find("not_found").text
    reply_markup.add(InlineKeyboardButton(
        text="Начать поиск сначала", callback_data="new_search"))

    try:
        return await query.message.edit_text(text, reply_markup=reply_markup)
    except MessageNotModified as e:
        logger.error(e)


@dp.callback_query_handler(lambda query: query.data.startswith(("fuel_type#")))
async def get_fuel_type(query: CallbackQuery) -> Message:
    fuel_type: str = re.sub("fuel_type#", "", query.data)
    if fuel_type == "any":
        globals.offer_metadata.IsAnyFuelType = True
    else:
        globals.offer_metadata.FuelType = fuel_type
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="По объему", callback_data="by_volume")],
            [InlineKeyboardButton(text="По мощности",
                                  callback_data="by_power")],
        ]
    )
    reply_markup.add(InlineKeyboardButton(
        text="Начать поиск сначала", callback_data="new_search"))
    return await query.message.edit_text(offer_page.find("select_volume_or_power").text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("by_volume")))
async def get_volume(query: CallbackQuery) -> None:
    globals.offer_metadata.IsVolume = True
    await query.message.edit_text(offer_page.find("min_volume").text)
    return await Volume.min.set()


@dp.message_handler(state=Volume.min)
async def get_min_volume(message: Message) -> Union[Message, None]:
    if not is_float(message.text):
        return await message.answer("Некорректный формат ввода!")
    globals.offer_metadata.MinVolume = message.text
    await message.answer(offer_page.find("max_volume").text)
    return await Volume.max.set()


@dp.message_handler(state=Volume.max)
async def get_max_volume(message: Message, state: FSMContext) -> Message:
    if not is_float(message.text):
        return await message.answer("Некорректный формат ввода!")
    elif float(message.text) < float(globals.offer_metadata.MinVolume):
        return await message.answer("Значение не должно быть меньше предыдущего!")
    globals.offer_metadata.MaxVolume = message.text

    await state.finish()
    globals.cars = await find_car()
    reply_markup = InlineKeyboardMarkup()
    if not globals.cars:
        text = "Ничего не найдено!"
    else:
        transmissions = await get_transmission(globals.cars)
        if not transmissions:
            text = "Ничего не найдено!"
        else:
            for transmission in transmissions:
                reply_markup.add(InlineKeyboardButton(
                    text=transmission, switch_inline_query_current_chat=transmission))
            text = offer_page.find("select_transmission").text
    reply_markup.add(InlineKeyboardButton(
        text="Начать поиск сначала", callback_data="new_search"))
    return await message.answer(text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda query: query.data.startswith(("by_power")))
async def get_power(query: CallbackQuery) -> None:
    globals.offer_metadata.IsPower = True
    await query.message.edit_text(offer_page.find("min_power").text)
    return await Power.min.set()


@dp.message_handler(state=Power.min)
async def get_min_power(message: Message) -> Union[Message, None]:
    if not is_int(message.text):
        return await message.answer("Некорректный формат ввода!")
    globals.offer_metadata.MinPower = message.text
    await message.answer(offer_page.find("max_power").text)
    return await Power.max.set()


@dp.message_handler(state=Power.max)
async def get_max_power(message: Message, state: FSMContext) -> Message:
    if not is_int(message.text):
        return await message.answer("Некорректный формат ввода!")
    elif int(message.text) < int(globals.offer_metadata.MinPower):
        return await message.answer("Значение не должно быть меньше предыдущего!")
    globals.offer_metadata.MaxPower = message.text
    await state.finish()
    globals.cars = await find_car()
    reply_markup = InlineKeyboardMarkup()
    if not globals.cars:
        text = "Ничего не найдено!"
    else:
        transmissions = await get_transmission(globals.cars)
        if not transmissions:
            text = "Ничего не найдено!"
        else:
            reply_markup = InlineKeyboardMarkup()
            for transmission in transmissions:
                reply_markup.add(InlineKeyboardButton(
                    text=transmission, switch_inline_query_current_chat=transmission))
            text = offer_page.find("select_transmission").text
    reply_markup.add(InlineKeyboardButton(
        text="Начать поиск сначала", callback_data="new_search"))
    return await message.answer(text, reply_markup=reply_markup)


@dp.inline_handler()
async def inline_echo(query: InlineQuery) -> Any:
    transmission: str = query.query
    n: int = 0
    items: list = []
    price_arr: dict = []
    mark_ids: list = []
    if not globals.response:
        return not_found(query)
    is_any = globals.response.get("is_any")
    for car in globals.cars:
        if car.get("transmission") == transmission:
            id: Any = car.get("id")
            title: Any = car.get("title")
            price: Any = car.get("price")
            image: Any = car.get("image")
            mark_id = car.get("mark_id")
            engine_volume: Any = car.get("engine_volume")
            engine_power: Any = car.get("engine_power")
            type_fuel: Any = car.get("engine_type_fuel")
            wd: Any = car.get("wd")
            special = car.get("special")
            item: InlineQueryResultArticle = InlineQueryResultArticle(id=id, title=title,
                                                                    input_message_content=InputTextMessageContent(
                                                                        title),
                                                                    description=(F"Цена: {int(price)}₽\t"
                                                                                F"Объем: {engine_volume}\t"
                                                                                F"Мощность: {engine_power}\t"
                                                                                F"Тип: {type_fuel},\t"
                                                                                F"{wd}"),
                                                                    hide_url=True, thumb_url=image)
            if is_any:
                if not price in price_arr and not mark_id in mark_ids:
                    mark_ids.append(mark_id)
                    items.append(item)
                    n += 1
            else:
                if not price in price_arr:
                    items.append(item)
                    n += 1
            price_arr.append(price)
            if n == MAX_SHOW:
                break
    return await globals.bot.answer_inline_query(query.id, items, cache_time=3)


@dp.callback_query_handler(lambda query: query.data == "new_search")
async def new_search(query: CallbackQuery) -> Message:
    globals.offer_metadata: OfferMetaData = OfferMetaData()
    # Get receive_offer tag from xml data.
    offer_page: Any = globals.root.find("receive_offer")
    try:
        return await query.message.edit_text(offer_page.find("select_price").text, reply_markup=choice_price_markup)
    except BadRequest:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        return await bot.send_message(chat_id=query.message.chat.id, text=offer_page.find("select_price").text, reply_markup=choice_price_markup)


async def find_car() -> Union[Any, None]:
    _ = globals.offer_metadata
    globals.response: dict = api_requests.find_car(
        body=_.Body, fuel_type=_.FuelType, **globals.offer_metadata.to_header())
    if not globals.response:
        return None
    else:
        cars: Union[Any, None] = globals.response.get("cars")
        return cars


async def get_transmission(cars: list) -> list:
    transmission = [car.get("transmission") for car in cars]
    counter = Counter(transmission)
    return list(counter)


async def not_found(query: InlineQuery) -> Any:
    thumb: str = "https://raw.githubusercontent.com/amtp1/CarPoint/main/image/thumb.png"
    not_found_item: InlineQueryResultArticle = InlineQueryResultArticle(
        id=-1, title="Автомобиль не найден!", input_message_content=InputTextMessageContent("Auto not found"),
        description="Нам не удалось найти автомобиль по данным параметрам.", hide_url=True, thumb_url=thumb)
    return await globals.bot.answer_inline_query(query.id, [not_found_item], cache_time=3)
