from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.adapters.sqlalchemy_db.models.base import Base


class Tokens(Base):
    """Модель токенов."""
    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['Users'] = relationship(
        back_populates='token',
        lazy='selectin'
    )
