from aiogram import types as aiotypes
from loguru import logger

from msu_atpase_storage.main import dp


@dp.errors_handler()
async def handle_app_error(update: aiotypes.Update, exception: Exception):
    logger.error("Unexpected error occurred {}", repr(exception))
    await update.message.answer(
        f"На сервере произошла ошибка {repr(exception)}. "
        "Напиши @Talianash "
        "с подробным описанием проблемы, и мы попробуем что-нибудь с этим сделать. "
        "https://github.com/churnikov/msu-atpase-storage/issues"
    )
