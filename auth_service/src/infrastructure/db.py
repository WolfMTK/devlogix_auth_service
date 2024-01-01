from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, declared_attr

from src.core import settings

engine = create_async_engine(url=settings.db_url.unicode_string(),
                             echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=Base)
