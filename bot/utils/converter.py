import re
from typing import Any


def is_float(obj: Any) -> bool:
    if re.match(r'^-?\d+(?:\.\d+)$', obj) is None:
        return False
    else:
        return True


def is_int(obj: Any) -> bool:
    try:
        int(obj)
        return True
    except ValueError:
        return False
