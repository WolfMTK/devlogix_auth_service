from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .di import init_dependencies
from .exception_handler import custom_exception_handler
from .routers import init_routers


def create_app() -> FastAPI:
    app = FastAPI()
    init_dependencies(app)
    app.exception_handler(RequestValidationError)(custom_exception_handler)
    init_routers(app)
    return app


app = create_app()
