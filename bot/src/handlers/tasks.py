import datetime as dt
import logging

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from services.date import correct_format_date, get_correct_date
from services.exceptions import InvalidNameTaskError
from services.tasks import TaskService
from .states import TaskAddingStates, TaskDeletingStates, TaskGettingStates

router = Router()


@router.message(StateFilter(None), Command('add_task'))
async def add_task(message: Message, state: FSMContext) -> None:
    logging.info('Пользователь применил команду /add_task')
    await message.answer('Введите название задачи, которую хотите добавить.')
    await state.set_state(TaskAddingStates.adding_name_task)


@router.message(TaskAddingStates.adding_name_task)
async def task_name_adding(message: Message, state: FSMContext) -> None:
    if message.text != '/stop':
        logging.info('Пользовать ввел название задачи')
        await state.update_data(name_task=message.text)
        await message.answer('Введите описание задачи.')
        await state.set_state(TaskAddingStates.adding_description_task)
    else:
        logging.info('Пользователь применил команду /stop')
        await message.answer('Добавление задачи отменено.')
        await state.clear()


@router.message(TaskAddingStates.adding_description_task)
async def task_description_adding(message: Message, state: FSMContext) -> None:
    if message.text != '/stop':
        logging.info('Пользовать ввел описание задачи')
        await state.update_data(description_task=message.text)
        await message.answer(
            'Введите время окончания задачи в формате: '
            'день:месяц:год:час:минуты.'
        )
        await state.set_state(TaskAddingStates.adding_task)
    else:
        logging.info('Пользователь применил команду /stop')
        await message.answer('Добавление задачи отменено.')
        await state.clear()


@router.message(TaskAddingStates.adding_task)
async def task_adding(message: Message,
                      state: FSMContext,
                      session_pool: async_sessionmaker) -> None:
    if message.text != '/stop':
        date = message.text.split(':')
        try:
            logging.info('Пользовать ввел корректную дату')
            time_end = await correct_format_date(date)
            data = await state.get_data()
            await TaskService().add_task(
                session_pool,
                user_id=str(message.from_user.id),
                name=data.get('name_task'),
                description=data.get('description_task'),
                time_end=time_end
            )
            logging.info('Задача добавилась в базу данных')
            await message.answer('Задача добавлена.')
            await state.clear()
        except ValueError:
            logging.info('Пользователь ввел неверную дату')
            await message.answer(
                'Неверный формат даты. Повторите попытку снова!'
            )
            await state.set_state(TaskAddingStates.adding_task)
    else:
        logging.info('Пользователь применил команду /stop')
        await message.answer('Добавление задачи отменено.')
        await state.clear()


@router.message(StateFilter(None), Command('delete_task'))
async def delete_task(message: Message, state: FSMContext) -> None:
    logging.info('Пользователь применил команду /delete_task')
    await message.answer('Введите название задачи, которую хотите удалить.')
    await state.set_state(TaskDeletingStates.deleting_name_task)


@router.message(TaskDeletingStates.deleting_name_task)
async def task_deleting(message: Message,
                        state: FSMContext,
                        session_pool: async_sessionmaker) -> None:
    if message.text != '/stop':
        try:
            await TaskService().delete_task(session_pool,
                                            user_id=str(message.from_user.id),
                                            name=message.text)
            logging.exception('Задача удалена')
            await message.answer('Задача удалена.')
            await state.clear()
        except InvalidNameTaskError as error:
            logging.exception(error)
            await message.answer(
                f'Задача с названием <b>{message.text}</b> отсутствует! '
                'Повторите снова!'
            )
    else:
        logging.info('Пользователь применил команду /stop')
        await message.answer('Удаление задачи отменено.')
        await state.clear()


@router.message(StateFilter(None), Command('get_task'))
async def get_task(message: Message, state: FSMContext) -> None:
    logging.info('Пользователь применил команду /get_task')
    await message.answer('Введите название задачи, которую хотите найти.')
    await state.set_state(TaskGettingStates.getting_name_task)


@router.message(TaskGettingStates.getting_name_task)
async def task_getting(message: Message,
                       state: FSMContext,
                       session_pool: async_sessionmaker) -> None:
    if message.text != '/stop':
        try:
            task = await TaskService().get_task(
                session_pool,
                user_id=str(message.from_user.id),
                name=message.text
            )
            time_end = task.time_end - dt.datetime.utcnow()
            await message.answer('<b>Описание задачи:</b>\n'
                                 f'\t{task.description}\n'
                                 '<b>Время окончания задачи:</b>\n'
                                 f'\t{await get_correct_date(time_end)}.')
            await state.clear()
        except InvalidNameTaskError as error:
            logging.exception(error)
            await message.answer(
                f'Задача с названием <b{message.text}</b> отсутствует! '
                'Повторите снова!'
            )
    else:
        logging.info('Пользователь применил команду /stop')
        await message.answer('Поиск задачи отменен.')
        await state.clear()


# TODO:
#  1. Добавить пагинацию;
#  2. Добавить кнопки.
@router.message(Command('get_tasks'))
async def get_tasks(message: Message,
                    session_pool: async_sessionmaker) -> None:
    tasks = await TaskService().get_tasks(session_pool,
                                          user_id=str(message.from_user.id))
    print(tasks)
    await message.answer('Задачи')
