from fastapi import FastAPI

from auth.core.base import Base  # noqa
from auth.main.ioc import UserIOC
from auth.user.adapters.stub_db import StubUserGateway
from auth.user.presentation.dependencies.gateway import new_user_gateway
from auth.user.presentation.interactor_factory import UserInteractorFactory
from auth.user.presentation.web.users import router
from .di import init_dependencies


def create_app() -> FastAPI:
    app = FastAPI()
    init_dependencies(app)
    app.dependency_overrides.update(
        {StubUserGateway: new_user_gateway,
         UserInteractorFactory: UserIOC}
    )
    app.include_router(router)
    return app
