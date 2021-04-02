from aiogram.dispatcher.filters.state import State, StatesGroup


class SaveFile(StatesGroup):
    file = State()
    tool = State()
    comment = State()
