import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from msu_atpase_storage.config import settings
from msu_atpase_storage.gdrive_ import GDrive

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.tg_token)
storage = MongoStorage()
dp = Dispatcher(bot, storage=storage)
gdrive = GDrive()


def main(dispatcher: Dispatcher):
    executor.start_polling(dispatcher, skip_updates=True)
