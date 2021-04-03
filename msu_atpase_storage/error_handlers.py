from aiogram import types as aiotypes
from loguru import logger

from msu_atpase_storage.main import dp


@dp.errors_handler()
async def handle_app_error(update: aiotypes.Update, exception: Exception):
    logger.error("Unexpected error occurred {}", repr(exception))
    await update.message.answer(
        f"На сервере произошла ошибка {repr(exception)}. "
        "Создайте, пожалуйста issue на github, "
        "с подробным описанием проблемы, и разработчики возьмутся за работу "
        "https://github.com/churnikov/msu-atpase-storage/issues"
    )
