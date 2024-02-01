import asyncio
from pathlib import Path
from functools import partial
from httpx import AsyncClient
import pytest
from mixer.backend.sqlalchemy import Mixer as _mixer
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

try:
    from app.app import app
except (NameError, ImportError):
    raise AssertionError('Не обнаружен объект `app`.')

try:
    from app.infrastructure.db import Base
except (NameError, ImportError):
    raise AssertionError('Не обнаружен объект `Base`')

try:
    from app.application.protocols.unit_of_work import UnitOfWork
except (NameError, ImportError):
    raise AssertionError('Не обнаружен объект `UnitOfWork`.')

try:
    from app.core.dependencies import unit_of_work
except (NameError, ImportError):
    raise AssertionError('Не обнаружен объект `unit_of_work`.')

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

TEST_DB = BASE_DIR / 'test.db'
SQLALCHEMY_DATABASE_URI = f'sqlite+aiosqlite:///{TEST_DB}'
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={'check_same_thread': False},
)
testing_async_session_maker = async_sessionmaker(engine,
                                                 expire_on_commit=False)

metadata = Base.metadata
metadata.bind = engine


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine.begin() as connect:
        await connect.run_sync(metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def async_client():
    app.dependency_overrides[unit_of_work] = partial(
        UnitOfWork,
        testing_async_session_maker
    )
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture
def mixer():
    mixer_engine = create_engine(f'sqlite:///{str(TEST_DB)}')
    session = sessionmaker(bind=mixer_engine)
    return _mixer(session=session(), commit=True)
