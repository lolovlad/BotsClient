from aiogram.types import Message, CallbackQuery, InputMediaPhoto, BufferedInputFile
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.utils.media_group import MediaGroupBuilder


from telegram.lexicorn import LEXICON_RU

from telegram.keyboards.reserver_keybords import (
    create_view_keybord
)
from telegram.database import main_db
from telegram.callbacks import TypeCommandPagination, CommandCallback

from telegram.Reposiotry.serverRepository import ServerRepository

from telegram.funct import create_view_reserver, create_weather_reserver


import base64
import io

router = Router()


@router.callback_query(TypeCommandPagination.filter())
async def pagination_view(clb: CallbackQuery,
                          callback_data: TypeCommandPagination):
    if clb.from_user.id in main_db:
        user_memory = main_db[clb.from_user.id]

        if callback_data.type_pagination == "prev":
            if user_memory["num_page"] - 1 == 0:
                await clb.answer(text=LEXICON_RU["denide"])
            else:
                user_memory["num_page"] -= 1
        else:
            if user_memory["num_page"] + 1 > user_memory["count_page"]:
                await clb.answer(text=LEXICON_RU["denide"])
            else:
                user_memory["num_page"] += 1

        repo = ServerRepository()

        view = await repo.get_page_reserver(user_memory["filters"]["type"]["val"],
                                            user_memory["filters"]["region"]["val"],
                                            user_memory["num_page"])

        await clb.message.edit_text(
            text=create_view_reserver(view),
            reply_markup=create_view_keybord(user_memory["num_page"], user_memory["count_page"], view["id"])
        )
    else:
        await clb.answer(text=LEXICON_RU["not_reg"])


@router.callback_query(CommandCallback.filter(F.type_command == "get_geoposition"))
async def command_geoposition_view(clb: CallbackQuery,
                                   callback_data: CommandCallback):
    if clb.from_user.id in main_db:
        user_memory = main_db[clb.from_user.id]

        repo = ServerRepository()

        view = await repo.get_one_reserver(callback_data.reserver_id)

        await clb.message.answer_location(
            latitude=view["x"],
            longitude=view["y"]
        )
    else:
        await clb.answer(text=LEXICON_RU["not_reg"])


@router.callback_query(CommandCallback.filter(F.type_command == "get_image"))
async def command_get_image_view(clb: CallbackQuery,
                                 callback_data: CommandCallback):
    if clb.from_user.id in main_db:
        user_memory = main_db[clb.from_user.id]

        repo = ServerRepository()

        view = await repo.get_one_reserver(callback_data.reserver_id)

        media = MediaGroupBuilder()

        for i in view["img"]:
            image_data = base64.b64decode(i["image"])
            image_io = io.BytesIO(image_data)
            image_io.seek(0)
            image_io.name = i["link"]

            media.add_photo(BufferedInputFile(file=image_io.read(), filename=i["link"]))

        return clb.message.answer_media_group(media=media.build())

    else:
        await clb.answer(text=LEXICON_RU["not_reg"])


@router.callback_query(CommandCallback.filter(F.type_command == "get_weather"))
async def command_get_weather_view(clb: CallbackQuery,
                                   callback_data: CommandCallback):
    if clb.from_user.id in main_db:
        user_memory = main_db[clb.from_user.id]

        repo = ServerRepository()

        view = await repo.get_weather(callback_data.reserver_id)

        await clb.message.answer(
            text=create_weather_reserver(view)
        )

    else:
        await clb.answer(text=LEXICON_RU["not_reg"])