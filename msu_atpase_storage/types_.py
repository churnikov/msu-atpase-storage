from dataclasses import dataclass

from aiogram.dispatcher.filters.state import State, StatesGroup


class SaveFile(StatesGroup):
    file = State()
    tool = State()
    comment = State()


@dataclass
class GDriveFile:
    filename: str
    link: str
    id_: str
