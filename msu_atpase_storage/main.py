import logging
from unittest.mock import MagicMock

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from msu_atpase_storage.config import settings
from msu_atpase_storage.gdrive_ import GDrive
from msu_atpase_storage.gspreadsh import GSheet

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.tg_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
gdrive = MagicMock()
gsheet = MagicMock()


def main(dispatcher: Dispatcher):
    executor.start_polling(dispatcher, skip_updates=True)
