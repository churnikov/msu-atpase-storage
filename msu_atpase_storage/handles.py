import json
import tempfile
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes, User
from loguru import logger

from msu_atpase_storage.id_gen import generate_id
from msu_atpase_storage.main import bot, dp, gdrive, gsheet
from msu_atpase_storage.types_ import GSheetRow, SaveFile


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    logger.info("User {} logged in", get_user_name(message.from_user))
    await message.reply(
        "Привет! Это бот для сохранения лабораторных данных. "
        "Ты можешь отправить ему файл, а он присвоит ему уникальный идентификатор, "
        "сохранит на гугл-диск и выдаст тебе постоянную ссылку для скачивания."
        " Снабжай файлы подробным описанием и делись идентификаторами "
        "с коллегами - это должно упростить поиск нужной информации.\n"
        "*Как пользоваться ботом?*\n"
        "Отправь боту сообщение с файлом, без текста."
        " Бот умеет воспринимать только один файл за раз, поэтому "
        "если хочется отправить сразу несколько файлов - "
        "выбери в телеграме опцию упаковки в zip-архив. После этого бот спросит, "
        "на каком приборе файл получен. Напиши ему ответное сообщение, например, 'Аминко'. "
        "Дальше бот попросит добавить к файлу комментарий. Не ограничивай себя! "
        "Чем подробнее будет описание, тем легче впоследствии будет тебе и твоим коллегам. "
        "Опиши, что за опыт ты проводил/а или прикрепи ссылку на подробное описание.\n"
        "[Журнал загрузки данных.](https://docs.google.com/spreadsheets/d/1pS"
        "-_5MRg70xQ6AFJJvEcuOiBTA-JbwL-ORFmxJraoss/edit?usp=sharing) "
        "(обрати внимание, из него тоже можно скачивать файлы)\n"
        "[Папка на гугл-диске с файлами.]("
        "https://drive.google.com/drive/folders/1QOn4cMpERteSUKZqaTK181pXg92QRN5a?usp=sharing)\n "
        "Если возникнут проблемы, пиши @Talianash.",
        parse_mode=types.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


@dp.message_handler(commands=["cancel"], state="*")
async def cancel_command(message: types.Message, state: FSMContext):
    """
    This handler will be called when user sends `/cancel`command.
    Cancels file upload process.
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    logger.info("User {} canceled state {}.", get_user_name(message.from_user), current_state)
    await state.finish()
    await message.reply("Отмена свершилась!", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def get_file(message: types.Message, state: FSMContext):
    """Starts the process of file upload. Triggered when user sent file."""
    async with state.proxy() as data:
        data["file"] = message.document.as_json()

    logger.info("User {} sent file", get_user_name(message.from_user))
    logger.debug("User {} sent file {}", get_user_name(message.from_user), data["file"])

    await SaveFile.tool.set()
    await message.answer("На каком приборе получены эти данные?")


@dp.message_handler(state=SaveFile.tool)
async def get_tool(message: types.Message, state: FSMContext):
    try:
        """Seconds step of file upload."""
        async with state.proxy() as data:
            data["tool"] = message.text

        logger.info(
            "User {user} said file {file_id} came from tool {tool}",
            user=get_user_name(message.from_user),
            file_id=json.loads(data["file"])["file_id"],
            tool=message.text,
        )

        await SaveFile.comment.set()
        await message.reply("Добавь описание: суть эксперимента, организм, условия и т.д.")
    except Exception as e:
        await state.finish()
        raise e


@dp.message_handler(state=SaveFile.comment)
async def get_comment(message: types.Message, state: FSMContext):
    """
    Part of file upload process.

    Downloads file, saves it in a tmp dir, uploads to gdrive and saves info to google spreadsheet
    """
    try:
        async with state.proxy() as data:
            data["comment"] = message.text

        await message.reply("Сохраняю файл")

        row_id = gsheet.get_next_free_row_id()
        file_id = generate_id(row_id - 2)
        file_json = json.loads(data["file"])

        logger.info(
            "User {user} for file with file_id: {file_id} added comment {comment}",
            user=get_user_name(message.from_user),
            file_id=file_json["file_id"],
            comment=message.text,
        )

        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp_file = Path(tmpdirname) / file_json["file_name"]
            await bot.download_file_by_id(file_json["file_id"], tmp_file)
            logger.info("Saved file {} to {}", file_json["file_id"], tmp_file)
            file = gdrive.upload_file(tmp_file, file_id)
            logger.info("Uploaded file {} to gdrive", file_json["file_id"])

        data = GSheetRow(
            file_id=file_id,
            tool=data["tool"],
            date=str(message.date),
            user=get_user_name(message.from_user),
            file_link=file.link,
            comment=data["comment"],
        )
        gsheet.add_row(data)
        logger.info("Saved data {} to gsheets", data)

        await message.reply("Файл сохранен!\n" + str(data), disable_web_page_preview=True)
    finally:
        await state.finish()


def get_user_name(user: User) -> str:
    """
    Construct username from `User` object of aiogram.
    Result is `user.full_name (user.username)`
    """
    name = user.full_name
    if user.username is not None:
        name += f" ({user.username})"
    return name
