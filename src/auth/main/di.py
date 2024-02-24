from functools import partial

from fastapi import FastAPI

from auth.application.protocols.unit_of_work import UoW, UnitOfWork
from auth.infrastructure.db import create_async_session_maker


def init_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[UoW] = partial(
        UnitOfWork,
        create_async_session_maker()
    )
