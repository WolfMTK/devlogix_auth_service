import uuid

from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    declared_attr,
)


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True,
        default=uuid.uuid4
    )

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()
