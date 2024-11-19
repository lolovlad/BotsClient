from aiogram import Bot
from aiogram.types import BotCommand

from telegram.lexicorn import LEXICON_COMMAND


async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command, description in LEXICON_COMMAND.items()]
    await bot.set_my_commands(main_menu_commands)