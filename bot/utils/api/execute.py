import requests

from log.logger import logger
from config.config import Config
from .headers import HEADERS, convert_to_headers
from .serializer import serialize_content


config = Config()

def make_request(path: str, headers=None, timeout=2, **kwargs) -> dict:
    if headers:
        HEADERS.update(convert_to_headers(**headers))
    if kwargs:
        values = [str(v) for v in kwargs.values()]
        args_string = "/".join(values)
        url = (rF"http://{config.host}:{config.port}/{path}{args_string}")
    else:
        url = (rF"http://{config.host}:{config.port}/{path}")
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    if response.status_code == 200:
        return serialize_content(response.content)
    else:
        return logger.error(response.content)