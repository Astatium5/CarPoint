import asyncio
import databases
import xml.etree.ElementTree as ET

import orm
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from log.logger import logger
from objects.globals import config
from objects import globals


async def main():
    globals.bot = Bot(token=config.token, parse_mode="HTML")
    globals.dp = Dispatcher(globals.bot, storage=MemoryStorage())

    bot_info: dict = await globals.bot.get_me()
    logger.info(F"Bot username: @{bot_info.username}, Bot ID: {bot_info.id}")

    tree = ET.parse('text/text.xml')
    globals.root = tree.getroot()

    # database = databases.Database(F"mysql+aiomysql://root:fG11xztk@localhost/carpointdb")
    # Connect to database
    # await database.connect()

    # globals.models = orm.ModelRegistry(database=database)
    # Create the tables
    # await globals.models.create_all()

    import commands

    await globals.dp.start_polling()

if __name__ == "__main__":
    try:
        main_loop = asyncio.get_event_loop()
        main_loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
