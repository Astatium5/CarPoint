import requests
from requests.exceptions import ReadTimeout, HTTPError

from log.logger import logger
from config.config import Config
from .headers import convert_to_headers
from .serializer import serialize_content

config: Config = Config()


def make_request(path: str, headers=None, timeout=7, **kwargs) -> dict:
    h = {'Content-Type': 'application/json',
         'Accept': 'application/json',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
    if headers:
        h.update(convert_to_headers(**headers))
    if kwargs:
        values: list = [str(v) for v in kwargs.values()]
        args_string: str = "/".join(values)
        url: str = rF"{config.host}/{path}{args_string}"
    else:
        url: str = rF"{config.host}/{path}"
    try:
        response = requests.get(url, headers=h, timeout=timeout, verify=False)
        if response.status_code == 200:
            return serialize_content(response.content)
        else:
            response.raise_for_status()
    except HTTPError as e:
        return logger.error(e)
    except ReadTimeout as e:
        return logger.error(e)
    except AssertionError as e:
        return logger.error(e)
    except UnicodeEncodeError as e:
        return logger.error(e)
