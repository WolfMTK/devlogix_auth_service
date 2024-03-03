from sqlalchemy.orm import Mapped, relationship, mapped_column

from auth.adapters.sqlalchemy_db.enums.roles import RoleEnum
from .association_tables import users_roles
from .base import Base


class Roles(Base):
    """Модель ролей."""
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[RoleEnum]
    user: Mapped[list['Users']] = relationship(
        secondary=users_roles,
        back_populates='roles',
        lazy='joined'
    )
