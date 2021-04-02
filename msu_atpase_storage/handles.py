import json
from io import BytesIO

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from msu_atpase_storage.id_gen import generate_id
from msu_atpase_storage.main import bot, dp
from msu_atpase_storage.types_ import SaveFile


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def get_file(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["file"] = message.document.as_json()

    await SaveFile.tool.set()
    await message.answer("С какого инструмента пришел файл?")


@dp.message_handler(state=SaveFile.tool)
async def get_tool(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["tool"] = message.text

    await SaveFile.comment.set()
    await message.reply("Добавь дополнительную информацию о файле в свободной форме")


@dp.message_handler(state=SaveFile.comment)
async def get_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["comment"] = message.text

    file_json = json.loads(data["file"])
    file = BytesIO()
    await bot.download_file_by_id(file_json["file_id"], file)
    await message.reply(
        "Проверим информацию перед сохранением:\n"
        f"Инструмент: {data['tool']}\n"
        f"Комментарий: {data['comment']}\n"
        f"Файл: {file_json['file_name']}\n"
        f"Файл id: {generate_id(6)}"
    )
    await state.finish()
