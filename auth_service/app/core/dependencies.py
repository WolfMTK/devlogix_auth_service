from typing import Annotated

from fastapi import Depends

from app.application.protocols.unit_of_work import UnitOfWork, UoW
from app.infrastructure.db import async_session_maker


def unit_of_work() -> UnitOfWork:
    return UnitOfWork(async_session_maker)


UoWDep = Annotated[UoW, Depends(unit_of_work)]
