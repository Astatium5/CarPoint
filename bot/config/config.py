import os
from dataclasses import dataclass

import dotenv
from dotenv import load_dotenv, find_dotenv


@dataclass
class Config:
    token: str
    host: str

    def __init__(self):
        load_dotenv(find_dotenv()) # Load all config from .env file.
        self.set_config() # Call set config function.

    def set_config(self):
        # Bot config data.
        self.token = os.getenv("BOT_TOKEN")
        self.host = os.getenv("HOST")

    def change_value(self, key, value):
        """ The function changes the value in the file by the key
        Parameters
        ----------
            key: str | int
            value: Any
        """

        os.environ[key] = value
        dotenv.set_key(dotenv.find_dotenv(), key, os.environ[key])
