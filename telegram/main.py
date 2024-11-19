import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from telegram.settiongs import settings

from telegram.handlers import main_handlers, filter_handler, view_reserver_handlers, chat_handlers


from keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')

    storage = MemoryStorage()

    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    dp.workflow_data.update()
    dp.startup.register(set_main_menu)

    dp.include_router(main_handlers.router)
    dp.include_router(filter_handler.router)
    dp.include_router(view_reserver_handlers.router)
    dp.include_router(chat_handlers.router)

    logger.info('Подключаем роутеры')

    logger.info('Подключаем миддлвари')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())