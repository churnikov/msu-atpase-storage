from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple

from aiogram.dispatcher.filters.state import State, StatesGroup


class SaveFile(StatesGroup):
    file = State()
    tool = State()
    protocol = State()
    organism = State()
    date_yes_no = State()
    date = State()
    comment = State()


@dataclass
class GDriveFile:
    filename: str
    link: str
    id_: str


class GSheetRow(NamedTuple):
    file_id: str
    tool: str
    protocol: str
    organism: str
    experiment_date: str
    date: str
    user: str
    file_link: str
    comment: str

    def __str__(self) -> str:
        return (
            f"File ID: {self.file_id}\n"
            f"Инструмент: {self.tool}\n"
            f"Протокол: {self.protocol}\n"
            f"Организм: {self.organism}\n"
            f"Дата эксперимента: {self.experiment_date}\n"
            f"Дата добавления: {self.date}\n"
            f"Пользователь: {self.user}\n"
            f"Ссылка на файл: {self.file_link}\n"
            f"Комментарий: {self.comment}"
        )


class Device(Enum):
    AMINCO_NEW = "Aminco новый"
    AMINCO_OLD = "Aminco старый"
    FLUORO = "Fluoro-Max"
    CLARIO = "CLARIOstar"
    CINTRA = "Cintra"
    OTHER = "Другой"


class Protocol(Enum):
    PHENOL = "ATPase, phenol red"
    NADH = "ATPase, NADH assay"
    LUCIFERASE = "ATPase, luciferase assay"
    ACMA = "ACMA"
    SYNTHESIS = "ATP synthesis"
    LUCIFERASE_CONC = "ATP concentration, luciferase assay"
    ATEAM = "ATeam"
    PAGE = "SDS-PAGE"
    PI = "Pi assay"
    GROWTH_CURVES = "Growth curves"
    ABS_SPECTRA = "Abs spectra"
    OTHER = "Другое"


class Organism(Enum):
    ECLOI = "E. coli"
    BSUBTITLIS = "B. subtilis"
    SCEREVISIAE = "S. cerevisiae"
    OTHER = "Другой"


class TodayOrNot(Enum):
    NO = "Нет"
    YES = "Да"
