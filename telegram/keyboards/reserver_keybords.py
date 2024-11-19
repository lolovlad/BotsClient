from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telegram.lexicorn import LEXICON_RU

from telegram.Reposiotry.serverRepository import ServerRepository
from telegram.callbacks.view_callback import TypeCommandPagination, CommandCallback
from telegram.database import main_db


def create_view_keybord(num: int, count: int, id_reserver: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(*[
            InlineKeyboardButton(
                text="<<",
                callback_data=TypeCommandPagination(type_pagination="prev").pack()
            ),
            InlineKeyboardButton(
                text=f"{num}/{count}",
                callback_data="sadasfdasdfgasfsa"
            ),
            InlineKeyboardButton(
                text=">>",
                callback_data=TypeCommandPagination(type_pagination="next").pack()
            ),
        ]
    )
    kb_builder.row(InlineKeyboardButton(
        text="Получить место на карте",
        callback_data=CommandCallback(type_command="get_geoposition", reserver_id=id_reserver).pack()
    ))

    kb_builder.row(InlineKeyboardButton(
        text="Посмотреть изображения",
        callback_data=CommandCallback(type_command="get_image", reserver_id=id_reserver).pack()
    ))

    kb_builder.row(InlineKeyboardButton(
        text="Погода в ближайшую неделю",
        callback_data=CommandCallback(type_command="get_weather", reserver_id=id_reserver).pack()
    ))

    return kb_builder.as_markup()