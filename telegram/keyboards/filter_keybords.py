from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telegram.lexicorn import LEXICON_RU

from telegram.Reposiotry.serverRepository import ServerRepository
from telegram.callbacks.filter_callback import RegionFilterCallback, TypeFilterCallback


def create_filter_menu_keyboard(buttons: list[dict]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for btn in buttons:
        kb_builder.row(
            InlineKeyboardButton(
                text=btn["name"],
                callback_data=btn["callback"]
            )
        )
    return kb_builder.as_markup()


async def create_region_filter_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    repo = ServerRepository()

    regions = await repo.get_region()

    for button in regions:
        kb_builder.row(InlineKeyboardButton(
            text=button['name'],
            callback_data=RegionFilterCallback(id_region=button['id']).pack()
        ))

    kb_builder.row(
        InlineKeyboardButton(
            text="Все",
            callback_data=RegionFilterCallback(id_region=0).pack()
        ),
        width=1
    )

    kb_builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_filter"
        ),
        width=1
    )
    return kb_builder.as_markup()


async def create_type_filter_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    repo = ServerRepository()

    types = await repo.get_type()

    for button in types:
        kb_builder.row(InlineKeyboardButton(
            text=button['name'],
            callback_data=TypeFilterCallback(id_type=button['id']).pack()
        ))

    kb_builder.row(
        InlineKeyboardButton(
            text="Все",
            callback_data=TypeFilterCallback(id_type=0).pack()
        ),
        width=1
    )

    kb_builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_filter"
        ),
        width=1
    )
    return kb_builder.as_markup()