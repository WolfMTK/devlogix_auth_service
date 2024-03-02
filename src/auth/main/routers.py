from fastapi import FastAPI

from auth.api import routers


def init_routers(app: FastAPI):
    """Инициализация роутеров."""
    for router in routers:
        app.include_router(router)
