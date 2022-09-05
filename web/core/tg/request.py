import os
from typing import Union, Dict, Any

import requests
from requests import Response


def sendQuestion(name, tel, text):
    text: str = (
        F"<b>Новый вопрос. (WEB)</b>\n"
        F"Имя: {name}\n"
        F"Телефон: {tel}\n"
        F"Вопрос: {text}"
    )
    bot_token: Union[str, None] = os.getenv("BOT_TOKEN")
    chat_id: Union[str, None] = os.getenv("CHAT_ID")
    url: str = F"https://api.telegram.org/bot{bot_token}/sendMessage?parse_mode=HTML"
    data: Dict[str, Any] = {'chat_id': chat_id, 'text': text}
    response: Response = requests.post(url, data=datas)
    return response


def leaveRequest(car_id, name, city, tel, email, address, is_new):
    host: Union[str, None] = os.getenv("HOST")
    if is_new:
        table_name: str = "newcar"
    else:
        table_name: str = "car"
    text: str = (
        F"<b>Новая заявка. (WEB)</b>\n"
        F"ID автомобиля: <code>{car_id}</code>\n"
        F"Эл. почта: <code>{email}</code>\n"
        F"Полное имя: <code>{name}</code>\n"
        F"Город: <code>{city}</code>\n"
        F"Номер телефона: <code>{tel}</code>\n"
        F"Адрес: <code>{address}</code>\n"
        F"Подробная информация об автомобиле: <code>{host}/admin/core/{table_name}/{car_id}/change</code>"
    )
    bot_token: Union[str, None] = os.getenv("BOT_TOKEN")
    chat_id: Union[str, None] = os.getenv("CHAT_ID")
    url: str = F"https://api.telegram.org/bot{bot_token}/sendMessage?parse_mode=HTML"
    data: Dict[str, Any] = {'chat_id': chat_id, 'text': text}
    response: Response = requests.post(url, data=data)
    return response
