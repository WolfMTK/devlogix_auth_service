import asyncio
from functools import partial
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

try:
    from auth.main import app
except (NameError, ImportError):
    raise AssertionError('Не обнаружен объект `app`.')
try:
    from auth.domain.models import Base
except (NameError, ImportError):
    raise AssertionError('Не обнаружен объект `Base`')
try:
    from auth.adapters.sqlalchemy_db.database import Session
except (NameError, ImportError):
    raise AssertionError('Не обнаружен объекты `Session`.')
try:
    from auth.application.protocols.database import UoWDatabase
except (NameError, ImportError):
    raise AssertionError('Не обнаружен объекты `UoWDatabase`.')

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

TEST_DB = BASE_DIR / 'test.db'
SQLALCHEMY_DATABASE_URI = f'sqlite+aiosqlite:///{TEST_DB}'
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={'check_same_thread': False},
)
testing_async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False
)

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


pytest_plugins = ['tests.fixtures.functions']


@pytest.fixture(scope='session')
async def async_client():
    app.dependency_overrides[UoWDatabase] = partial(
        Session,
        testing_async_session_maker
    )
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
