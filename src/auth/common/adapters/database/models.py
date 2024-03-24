from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()
