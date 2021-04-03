import json
import tempfile
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes, User

from msu_atpase_storage.id_gen import generate_id
from msu_atpase_storage.main import bot, dp, gdrive, gsheet
from msu_atpase_storage.types_ import GSheetRow, SaveFile


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
    await message.answer("С какого прибора пришел файл?")


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

    row_id = gsheet.get_next_free_row_id()
    file_id = generate_id(row_id - 1)

    file_json = json.loads(data["file"])
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_file = Path(tmpdirname) / file_json["file_name"]
        await bot.download_file_by_id(file_json["file_id"], tmp_file)
        file = gdrive.upload_file(tmp_file, file_id)

    data = GSheetRow(
        file_id=file_id,
        tool=data["tool"],
        date=str(message.date),
        user=get_user_name(message.from_user),
        file_link=file.link,
        comment=data["comment"],
    )
    gsheet.add_row(data, row_id)

    await message.reply("Файл сохранен\n" + str(data))
    await state.finish()


def get_user_name(user: User) -> str:
    name = user.full_name
    if user.username is not None:
        name += f" ({user.username})"
    return name
