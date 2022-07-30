from typing import Any


def is_float(obj: Any) -> bool:
    try:
        float(obj)
        return True
    except ValueError:
        return False


def is_int(obj: Any) -> bool:
    try:
        int(obj)
        return True
    except ValueError:
        return False
