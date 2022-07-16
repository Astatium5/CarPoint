from aiogram.dispatcher.filters.state import StatesGroup, State


class Meeting(StatesGroup):
    name = State()
    city = State()


class ReceiveOffer(StatesGroup):
    phone = State()
    phone_string = State()


class Volume(StatesGroup):
    first_part = State()
    second_part = State()