import datetime as dt
import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import true

from auth.adapters.sqlalchemy_db.models.association_tables import users_roles
from auth.adapters.sqlalchemy_db.models.base import Base
from auth.application.models.users import UserGet


class Users(Base):
    """Модель пользователей."""
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True,
        default=uuid.uuid4
    )
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
        schema = UserGet()
        for key, value in vars(self).items():
            if hasattr(schema, key):
                setattr(schema, key, value)
        return schema
