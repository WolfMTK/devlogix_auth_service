from aiogram.fsm.state import State, StatesGroup


class TaskAddingStates(StatesGroup):
    adding_name_task = State()
    adding_description_task = State()
    adding_task = State()


class TaskDeletingStates(StatesGroup):
    deleting_name_task = State()


class TaskGettingStates(StatesGroup):
    getting_name_task = State()
