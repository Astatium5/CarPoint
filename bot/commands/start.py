import hashlib
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from aiogram.dispatcher.storage import FSMContext
from requests import request


from objects.globals import dp, bot
from objects import globals
from utils.api.requests import Requests
from .meeting import *
from states.states import *


api_requests = Requests()


@dp.message_handler(commands="start")
async def start(message: Message, state: FSMContext):
    globals.start = start
    await state.finish()
    response = api_requests.create_user(user_id=message.from_user.id, first_name=message.from_user.first_name,
        username=message.from_user.username) # Create new user

    bot_info = await bot.get_me() # Get bot info
    welcome_page = globals.root.find("welcome")

    if not response.get("response"):
        if not response.get("name"):
            await message.answer(welcome_page.find("is_empty").text.format(bot_info.first_name))
            return await Meeting.name.set()
        elif not response.get("city"):
            await message.answer(welcome_page.find("is_not_city").text)
            return await Meeting.city.set()
        else:
            reply_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                keyboard=[
                    [KeyboardButton(text="Получить предложение"), KeyboardButton(text="Для инвесторов")],
                    [KeyboardButton(text="Контакты"), KeyboardButton(text="О проекте"), KeyboardButton(text="Для дистрибьюторов")]
                ])
            return await message.answer(welcome_page.find("is_not_empty").text.format(bot_info.first_name),
                reply_markup=reply_markup)
    else:
        await message.answer(welcome_page.find("is_empty").text.format(bot_info.first_name))
        return await Meeting.name.set()

"""
@dp.inline_handler()
async def inline_echo(query: InlineQuery):
    items = []
    text = query.query or 'echo'
    input_content = InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=f'Result {text!r}',
        input_message_content=input_content,
    )
    items.append(item)
    await globals.bot.answer_inline_query(query.id, results=items, cache_time=1)

    r = InlineQueryResultArticle(id='1', title='SONY VTC6 3000 mah 30A 18650',  input_message_content=InputTextMessageContent('Аккумулятор 1'), description='blah', hide_url=True, thumb_url='https://via.placeholder.com/50')
    r2 = InlineQueryResultArticle(id='2', title='SONY VTC5A 2600 mah 35A 18650',  input_message_content=InputTextMessageContent('Аккумулятор 2'), description='blah', hide_url=True, thumb_url='https://via.placeholder.com/50')
    await globals.bot.answer_inline_query(query.id, [r, r2])
"""
