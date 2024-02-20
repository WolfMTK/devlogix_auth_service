from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
    Mapped,
    mapped_column,
)

from auth.core import Settings

engine = create_async_engine(
    url=Settings.db_url,
    echo=False
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base:
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=Base)
