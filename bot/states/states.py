from aiogram.dispatcher.filters.state import StatesGroup, State


class Meeting(StatesGroup):
    name = State()
    city = State()


class ReceiveOffer(StatesGroup):
    phone = State()
    phone_string = State()