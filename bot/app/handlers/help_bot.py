from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command('help'))
async def help_bot(message: Message):
    await message.answer('Добавление задачи: /add_task;\n'
                         'Вывести описание задачи: /get_task;\n'
                         'Вывести все доступные задачи: /get_tasks;\n'
                         'Удаление задачи: /delete_task;\n'
                         'Обновление задачи: /update_task;\n'
                         'Добавление заметок: /add;\n'
                         'Обновление заметок: /update;\n'
                         'Удаление заметок: /delete.')
