from dataclasses import dataclass
from typing import NamedTuple

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


class GSheetRow(NamedTuple):
    file_id: str
    tool: str
    date: str
    user: str
    file_link: str
    comment: str

    def __str__(self) -> str:
        return (
            f"File ID: {self.file_id}\n"
            f"Инструмент: {self.tool}\n"
            f"Дата добавления: {self.date}\n"
            f"Пользователь: {self.user}\n"
            f"Ссылка на файл: {self.file_link}\n"
            f"Комментарий: {self.comment}"
        )
