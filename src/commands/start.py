import hashlib
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher.storage import FSMContext


from objects.globals import dp
from objects import globals


@dp.message_handler(commands="start")
async def start(msg: Message, state: FSMContext):
    await state.finish()

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Search", switch_inline_query_current_chat="")]
        ]
    )

    return await msg.answer(
        text=F"Hello, I'm bot!", reply_markup=markup)

@dp.inline_handler()
async def inline_echo(query: InlineQuery):
    """
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
    """

    r = InlineQueryResultArticle(id='1', title='SONY VTC6 3000 mah 30A 18650',  input_message_content=InputTextMessageContent('Аккумулятор 1'), description='blah', hide_url=True, thumb_url='https://via.placeholder.com/50')
    r2 = InlineQueryResultArticle(id='2', title='SONY VTC5A 2600 mah 35A 18650',  input_message_content=InputTextMessageContent('Аккумулятор 2'), description='blah', hide_url=True, thumb_url='https://via.placeholder.com/50')
    await globals.bot.answer_inline_query(query.id, [r, r2])
