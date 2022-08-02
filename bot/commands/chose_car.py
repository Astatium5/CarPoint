from typing import Any

from aiogram.types import ChosenInlineResult, InlineKeyboardMarkup, InlineKeyboardButton

from utils.api.requests import Requests
from objects.globals import dp, bot


api_requests: Requests = Requests()  # Init Requests object.


@dp.chosen_inline_handler(lambda chosen_inline_result: True)
async def chosen_inline_result_handler(chosen_result: ChosenInlineResult) -> Any:
    if chosen_result.result_id != -1:
        response = api_requests.get_car_info(id=chosen_result.result_id)
        car = response.get("car")
        title = car.get("title")
        price = int(car.get("price"))
        image = car.get("image")
        engine_volume = car.get("engine_volume")
        engine_power = car.get("engine_power")
        engine_type_fuel = car.get("engine_type_fuel")
        wd = car.get("wd")
        expenditure = car.get("expenditure")
        transmission = car.get("transmission")
        text_page = (F"Название: <b>{title}</b>\n"
                     F"Цена: {price}₽\n"
                     F"Объем двигателя: {engine_volume}\n"
                     F"Мощность двигателя: {engine_power}\n"
                     F"Тип двигателя: {engine_type_fuel}\n"
                     F"Привод: {wd}\n"
                     F"Расход: {expenditure}\n"
                     F"Коробка: {transmission}")
        reply_markup = InlineKeyboardMarkup(inline_keyboard=[
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
