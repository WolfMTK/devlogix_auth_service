from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()
