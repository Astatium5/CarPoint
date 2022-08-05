from typing import Any

HEADERS: dict = {'Content-Type': 'application/json',
           'Accept': 'application/json',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}


def convert_to_headers(**kwargs) -> dict:
    for k, v in kwargs.items():
        if isinstance(v, bool) or isinstance(v, int) or isinstance(v, float):
            kwargs[k] = str(v)
    return kwargs
