from aiogram import Dispatcher, Bot

from config.config import Config

config: Config = Config()  # Init config object.

bot: Bot = None  # Set bot object without initialize.
dp: Dispatcher = None  # Set dispatcher object without initialize.

root = None # Xml data from local file.

# Receive offer state variables.
user_id: int = None # State user id.
phone = None # User phone.

prfp = None # Price range first part.
prsp = None # Price range second part.

start = None