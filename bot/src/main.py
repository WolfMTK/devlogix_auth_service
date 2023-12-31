import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from infrastructure.database.db import session_maker
from handlers import routers
from middlewares.db import DBSessionMiddleware
from middlewares.throttling import ThrottlingMiddleware
from core import config
from core.logging_config import configure_logging


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Начать работу с ботом'),
        BotCommand(command='/help', description='Помощь по командам'),
        BotCommand(command='/clear', description='Удаление информации'),
        BotCommand(command='/stop', description='Отменить команду')
    ]
    await bot.set_my_commands(commands=commands,
                              scope=BotCommandScopeAllPrivateChats())


async def main():
    configure_logging(Path(__file__).parent / 'logs')
    bot = Bot(config.bot_token, parse_mode='HTML')

    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(ThrottlingMiddleware(config.throttle_time_spin,
                                               config.throttle_time_other))
    dp.update.middleware(DBSessionMiddleware(session_pool=session_maker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    for router in routers:
        dp.include_router(router)

    try:
        logging.info('Запуск бота.')
        await set_commands(bot)
        await dp.start_polling(bot,
                               allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
