from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext


from telegram.lexicorn import LEXICON_RU
from telegram.database import main_db

from telegram.keyboards.filter_keybords import create_filter_menu_keyboard
from telegram.keyboards.reserver_keybords import create_view_keybord

from telegram.Reposiotry.serverRepository import ServerRepository

from telegram.funct import create_view_reserver
from telegram.fsm import FSMBot

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    if message.from_user.id not in main_db:
        repo = ServerRepository()
        count = await repo.get_num_page("all", "all")
        main_db[message.from_user.id] = {
            "filters": {
                "region": {
                    "name": "все",
                    "val": "all"
                },
                "type": {
                    "name": "все",
                    "val": "all"
                }
            },
            "num_page": 1,
            "count_page": count
        }
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands='help'))
async def process_help_command(message: Message, ):
    await message.answer(text=LEXICON_RU["/help"])


@router.message(Command(commands='get_reserve'))
async def process_reserve_command(message: Message, state: FSMContext):
    if message.from_user.id in main_db:
        user_memory = main_db[message.from_user.id]
        repo = ServerRepository()

        view = await repo.get_page_reserver(user_memory["filters"]["type"]["val"],
                                            user_memory["filters"]["region"]["val"],
                                            user_memory["num_page"])
        await message.answer(
            text=create_view_reserver(view),
            reply_markup=create_view_keybord(user_memory["num_page"], user_memory["count_page"], view["id"])
        )
        await state.set_state(FSMBot.get_reserve)
    else:
        await message.answer(text=LEXICON_RU["not_reg"])


@router.message(Command(commands='set_filter'))
async def process_filter_command(message: Message, state: FSMContext):
    if message.from_user.id in main_db:
        user_memory = main_db[message.from_user.id]
        user_memory["num_page"] = 1
        await message.answer(
            text="Настройки фильтра поиска",
            reply_markup=create_filter_menu_keyboard([
                {"name": f"Регион: {user_memory['filters']['region']["name"]}", "callback": "region"},
                {"name": f"Тип: {user_memory['filters']['type']["name"]}", "callback": "type"},
            ])
        )
        await state.set_state(FSMBot.set_filter)
    else:
        await message.answer(text=LEXICON_RU["not_reg"])


@router.message(Command(commands="start_chat"))
async def process_start_chat(message: Message, state: FSMContext):
    if message.from_user.id in main_db:

        await message.answer(
            text="Вы перешли в режим разговора с помошником\n"
                 "Напишити интересующий вас вопрос и помошник постараеться на него ответить"
        )
        await state.set_state(FSMBot.chat_n)
    else:
        await message.answer(text=LEXICON_RU["not_reg"])


@router.message(Command(commands="exit_chat"), StateFilter(FSMBot.chat_n))
async def process_start_chat(message: Message, state: FSMContext):
    if message.from_user.id in main_db:

        await state.clear()

        await message.answer(
            text="Вы вышли из режима чата"
        )
    else:
        await message.answer(text=LEXICON_RU["not_reg"])