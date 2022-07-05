import os
from dataclasses import dataclass

import dotenv
from dotenv import load_dotenv, find_dotenv


@dataclass
class Config:
    token: str

    def __init__(self):
        load_dotenv(find_dotenv())
        self.set_config()

    def set_config(self):
        self.token = os.getenv("BOT_TOKEN")

    def change_value(self, key, value):
        os.environ[key] = value
        dotenv.set_key(dotenv.find_dotenv(), key, os.environ[key])
