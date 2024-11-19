from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from telegram.lexicorn import LEXICON_RU
from aiogram.fsm.context import FSMContext

from telegram.database import main_db
from telegram.callbacks import TypeCommandPagination, CommandCallback

from telegram.Reposiotry.serverRepository import ServerRepository

from telegram.funct import create_view_reserver
from telegram.fsm import FSMBot

router = Router()


@router.message(StateFilter(FSMBot.chat_n), F.text)
async def get_answer(message: Message, state: FSMContext):
    if message.from_user.id in main_db:
        query = message.text
        service = ServerRepository()

        mes_chat = await message.answer(text="Ждем ответ от помошника")

        answer = await service.get_answer(query)
        await mes_chat.edit_text(text=answer["answer"])
        for i in answer["content"]:
            await message.answer(
                text=create_view_reserver(i),
            )

    else:
        await message.answer(text=LEXICON_RU["not_reg"])