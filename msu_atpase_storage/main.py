import logging

from aiogram import Bot, Dispatcher, executor, types

from msu_atpase_storage.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.tg_token)
dp = Dispatcher(bot)


def main(dp):
    executor.start_polling(dp, skip_updates=True)
