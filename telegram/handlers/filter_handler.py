from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from telegram.fsm import FSMBot
from telegram.lexicorn import LEXICON_RU

from telegram.keyboards.filter_keybords import (
    create_region_filter_keyboard,
    create_filter_menu_keyboard,
    create_type_filter_keyboard
)
from telegram.database import main_db
from telegram.callbacks import RegionFilterCallback, TypeFilterCallback

from telegram.Reposiotry.serverRepository import ServerRepository

router = Router()


@router.callback_query(F.data == 'region')
async def get_menu_region_filter(clb: CallbackQuery):
    if clb.from_user.id in main_db:
        user_memory = main_db[clb.from_user.id]

        kb = await create_region_filter_keyboard()

        await clb.message.edit_text(
            text="Выберите регион",
            reply_markup=kb
        )
    else:
        await clb.answer(text=LEXICON_RU["not_reg"])


@router.callback_query(F.data == 'back_filter')
async def back_filter(clb: CallbackQuery):
    if clb.from_user.id in main_db:
        user_memory = main_db[clb.from_user.id]
        await clb.message.edit_text(
            text="Настройки фильтра поиска",
            reply_markup=create_filter_menu_keyboard([
                {"name": f"Регион: {user_memory['filters']['region']["name"]}", "callback": "region"},
                {"name": f"Тип: {user_memory['filters']['type']["name"]}", "callback": "type"},
            ])
        )
    else:
        await clb.answer(text=LEXICON_RU["not_reg"])


@router.callback_query(RegionFilterCallback.filter())
async def set_new_reg_filter(clb: CallbackQuery,
                             callback_data: RegionFilterCallback):
    if clb.from_user.id in main_db:
        user_memory = main_db[clb.from_user.id]

        if callback_data.id_region > 0:
            entity = await ServerRepository().get_one_region(callback_data.id_region)
        else:
            entity = {
                "name": "Все",
                "id": "all"
            }

        main_db[clb.from_user.id]["filters"]["region"] = {
            "name": entity["name"],
            "val": entity["id"]
        }

        repo = ServerRepository()
        count = await repo.get_num_page(main_db[clb.from_user.id]["filters"]["type"]["val"], main_db[clb.from_user.id]["filters"]["region"]["val"])
        main_db[clb.from_user.id]["count_page"] = count

        await clb.message.edit_text(
            text="Настройки фильтра поиска",
            reply_markup=create_filter_menu_keyboard([
                {"name": f"Регион: {user_memory['filters']['region']["name"]}", "callback": "region"},
                {"name": f"Тип: {user_memory['filters']['type']["name"]}", "callback": "type"},
            ])
        )
    else:
        await clb.answer(text=LEXICON_RU["not_reg"])


@router.callback_query(F.data == 'type')
async def get_menu_type_filter(clb: CallbackQuery):
    if clb.from_user.id in main_db:
        kb = await create_type_filter_keyboard()

        await clb.message.edit_text(
            text="Выберите тип",
            reply_markup=kb
        )
    else:
        await clb.answer(text=LEXICON_RU["not_reg"])


@router.callback_query(TypeFilterCallback.filter())
async def set_new_reg_filter(clb: CallbackQuery,
                             callback_data: TypeFilterCallback):
    if clb.from_user.id in main_db:
        user_memory = main_db[clb.from_user.id]

        if callback_data.id_type > 0:
            entity = await ServerRepository().get_one_type(callback_data.id_type)
        else:
            entity = {
                "name": "Все",
                "id": "all"
            }

        main_db[clb.from_user.id]["filters"]["type"] = {
            "name": entity["name"],
            "val": entity["id"]
        }

        repo = ServerRepository()
        count = await repo.get_num_page(main_db[clb.from_user.id]["filters"]["type"]["val"], main_db[clb.from_user.id]["filters"]["region"]["val"])
        main_db[clb.from_user.id]["count_page"] = count

        await clb.message.edit_text(
            text="Настройки фильтра поиска",
            reply_markup=create_filter_menu_keyboard([
                {"name": f"Регион: {user_memory['filters']['region']["name"]}", "callback": "region"},
                {"name": f"Тип: {user_memory['filters']['type']["name"]}", "callback": "type"},
            ])
        )
    else:
        await clb.answer(text=LEXICON_RU["not_reg"])