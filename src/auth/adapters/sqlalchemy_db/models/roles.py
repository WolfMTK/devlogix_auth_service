from sqlalchemy.orm import Mapped, relationship

from auth.adapters.sqlalchemy_db.enums.roles import RoleEnum
from .association_tables import users_roles
from .base import Base


class Roles(Base):
    """Модель ролей."""
    name: Mapped[RoleEnum]
    user: Mapped[list['Users']] = relationship(
        secondary=users_roles,
        back_populates='roles',
        lazy='joined'
    )
