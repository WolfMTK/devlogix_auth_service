import datetime as dt

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import true

from auth.adapters.sqlalchemy_db.models.association_tables import users_roles
from auth.adapters.sqlalchemy_db.models.base import Base
from auth.application.models.users import UserGet


class Users(Base):
    """Модель пользователей."""
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        index=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        index=True
    )
    password: Mapped[str] = mapped_column(nullable=False)
    token: Mapped['Tokens'] = relationship(
        back_populates='user',
        lazy='selectin',
    )
    roles: Mapped[list['Roles']] = relationship(
        secondary=users_roles,
        back_populates='user',
        lazy='joined'
    )
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now())
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        server_default=true()
    )

    def set_empty_attributes(self) -> None:
        self.last_name = None  # noqa
        self.first_name = None  # noqa

    def to_read_model(self) -> UserGet:
        return UserGet(
            id=self.id,
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            is_active=self.is_active
        )