import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from services.users import UsersService

router = Router()


@router.message(CommandStart())
async def start(message: Message, session_pool: async_sessionmaker):
    logging.info('Пользователь применил комманду /start!')
    user_id = message.from_user.id
    user = await UsersService().get_user(session_pool, user_id=str(user_id))
    if not user:
        username = message.from_user.username
        await UsersService().add_user(session_pool,
                                      user_id=user_id,
                                      username=username)
        logging.info(f'Новый пользователь {username} добавлен в БД!')
    await message.answer(f'Привет, {message.from_user.full_name}!\n'
                         'Помощь по командам: /help.')
