from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.core.base import Base  # noqa
from auth.main.di import init_dependencies
from auth.main.ioc import UserIOC, TokeIOC
from auth.token.adapters.stub_db import StubTokenGateway
from auth.token.presentation.dependencies.gateway import new_token_gateway
from auth.token.presentation.interactor_factory import TokenInteractorFactory
from auth.user.adapters.stub_db import StubUserGateway
from auth.user.presentation.dependencies.gateway import new_user_gateway
from auth.user.presentation.interactor_factory import UserInteractorFactory
from auth.user.presentation.web import user, auth


def set_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['GET', 'POST', 'PATCH', 'DELETE'],
        allow_headers=['*']
    )


def create_app() -> FastAPI:
    app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})
    set_middleware(app)
    init_dependencies(app)
    app.dependency_overrides.update(
        {StubUserGateway: new_user_gateway,
         StubTokenGateway: new_token_gateway,
         UserInteractorFactory: UserIOC,
         TokenInteractorFactory: TokeIOC}
    )
    app.include_router(user.router)
    app.include_router(auth.router)
    return app
