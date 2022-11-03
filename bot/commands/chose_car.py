from typing import Any, Union

from aiogram.types import ChosenInlineResult, InlineKeyboardMarkup, InlineKeyboardButton

from utils.api.requests import Requests
from objects.globals import dp, bot

api_requests: Requests = Requests()  # Init Requests object.


@dp.chosen_inline_handler(lambda chosen_inline_result: True)
async def chosen_inline_result_handler(chosen_result: ChosenInlineResult) -> Any:
    if chosen_result.result_id != -1:
        response: dict = api_requests.get_car_info(id=chosen_result.result_id)
        car: Union[Any, None] = response.get("car")
        title: Any = car.get("title")
        price: Any = int(car.get("price"))
        image: Any = car.get("image")
        engine_volume: Any = car.get("engine").get("volume")
        engine_power: Any = car.get("engine").get("power")
        engine_type_fuel: Any = car.get("engine").get("type_fuel")
        wd: Any = car.get("wd")
        expenditure: Any = car.get("expenditure")
        transmission: Any = car.get("transmission")
        text_page: str = (F"Название: <b>{title}</b>\n"
                     F"Цена: {price}₽\n"
                     F"Объем двигателя: {engine_volume}\n"
                     F"Мощность двигателя: {engine_power}\n"
                     F"Тип двигателя: {engine_type_fuel}\n"
                     F"Привод: {wd}\n"
                     F"Расход: {expenditure}\n"
                     F"Коробка: {transmission}")
        reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Оставить заявку", callback_data=F"leave_request#{chosen_result.result_id}")]
        ])
        reply_markup.add(InlineKeyboardButton(
            text="Начать поиск сначала", callback_data="new_search"))
        try:
            return await bot.send_photo(chosen_result.from_user.id, photo=image, caption=text_page, reply_markup=reply_markup)
        except:
            text_page += image
            return await bot.send_message(chosen_result.from_user.id, text_page, reply_markup=reply_markup)
