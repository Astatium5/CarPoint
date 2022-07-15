import requests

from log.logger import logger
from config.config import Config
from .headers import HEADERS
from .serializer import serialize_content


config = Config()

def make_request(path: str, **kwargs):
    values = [str(v) for v in kwargs.values()]
    args_string = "/".join(values)
    url = (rF"http://{config.host}:{config.port}/{path}{args_string}")
    response = requests.get(url, headers=HEADERS, timeout=0.5)
    if response.status_code == 200:
        return serialize_content(response.content)
    else:
        return logger.error(response.content)