from functools import partial
from typing import Annotated

from fastapi import Depends

from src.application.protocols.unit_of_work import UoW, UnitOfWork
from src.infrastructure.db import async_session_maker

UOWDep = Annotated[UoW, Depends(partial(UnitOfWork, async_session_maker))]
