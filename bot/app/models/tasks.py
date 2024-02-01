import datetime as dt

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.db import Base


class Tasks(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    time_end: Mapped[dt.datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self):
        return f'Tasks({self.name})'
