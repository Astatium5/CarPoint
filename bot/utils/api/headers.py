from typing import Any


def convert_to_headers(**kwargs) -> dict:
    for k, v in kwargs.items():
        if isinstance(v, bool) or isinstance(v, int) or isinstance(v, float):
            kwargs[k] = str(v)
    return kwargs
