from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from infrastructure.database.db import Base


class Users(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str]
    user_id: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    # tasks: Mapped[list['Tasks']] = relationship(back_populates='users',
    #                                             lazy='joined')

    def __repr__(self):
        return f'Users({self.username})'
