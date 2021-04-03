import json
import tempfile
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from msu_atpase_storage.id_gen import generate_id
from msu_atpase_storage.main import bot, dp, gdrive
from msu_atpase_storage.types_ import SaveFile


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def get_file(message: types.Message, state: FSMContext):
    """Starts the process of file upload. Triggered when user sent file."""
    async with state.proxy() as data:
        data["file"] = message.document.as_json()

    await SaveFile.tool.set()
    await message.answer("С какого инструмента пришел файл?")


@dp.message_handler(state=SaveFile.tool)
async def get_tool(message: types.Message, state: FSMContext):
    """Seconds step of file upload."""
    async with state.proxy() as data:
        data["tool"] = message.text

    await SaveFile.comment.set()
    await message.reply("Добавь дополнительную информацию о файле в свободной форме")


@dp.message_handler(state=SaveFile.comment)
async def get_comment(message: types.Message, state: FSMContext):
    """
    Part of file upload process.

    Downloads file, saves it in a tmp dir, uploads to gdrive and saves info to google spreadsheet
    """
    async with state.proxy() as data:
        data["comment"] = message.text

    await message.reply("Сохраняю файл")

    file_id = generate_id(len(gdrive.list_files()))

    file_json = json.loads(data["file"])
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_file = Path(tmpdirname) / file_json["file_name"]
        await bot.download_file_by_id(file_json["file_id"], tmp_file)
        file = gdrive.upload_file(tmp_file, file_id)

    await message.reply(
        "Файл сохранен\n"
        f"Инструмент: {data['tool']}\n"
        f"Комментарий: {data['comment']}\n"
        f"Файл: {file_json['file_name']}\n"
        f"Файл на GoogleDrive: {file.filename}\n"
        f"Файл id: {file_id}\n"
        f"Ссылка на файл: {file.link}"
    )
    await state.finish()
