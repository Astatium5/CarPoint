from typing import Any

from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

MAX_SHOW: int = 20

def filter(cars: list, transmission: str, is_any: bool, n: int = 0):
    items: list = []
    prices: list = []
    marks_id: list = []
    for car in cars:
        if car.get("transmission") == transmission:
            id: Any = car.get("id")
            title: Any = car.get("title")
            price: Any = car.get("price")
            image: Any = car.get("image")
            mark_id = car.get("mark_id")
            engine_volume: Any = car.get("engine").get("volume")
            engine_power: Any = car.get("engine").get("power")
            type_fuel: Any = car.get("engine").get("type_fuel")
            wd: Any = car.get("wd")
            item: InlineQueryResultArticle = InlineQueryResultArticle(
                id=id, title=title, input_message_content=InputTextMessageContent(title),
                description=(F"Цена: {int(price)}₽\t"
                             F"Объем: {engine_volume}\t"
                             F"Мощность: {engine_power}\t"
                             F"Тип: {type_fuel},\t"
                             F"{wd}"),
                hide_url=True, thumb_url=image)
            if is_any:
                if price not in prices and mark_id not in marks_id:
                    marks_id.append(mark_id)
                    items.append(item)
                    n += 1
            else:
                if price not in prices:
                    items.append(item)
                    n += 1
            prices.append(price)
            if n == MAX_SHOW:
                break
    return items
