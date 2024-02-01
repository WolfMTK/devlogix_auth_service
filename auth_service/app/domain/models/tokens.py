from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db import Base


class RefreshToken(Base):
    """Модель refresh_token."""
    __tablename__ = 'refresh_token'
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True,
                                       nullable=False,
                                       index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='refresh_token',
                                        lazy='selectin')


class AccessToken(Base):
    """Модель access_token."""
    __tablename__ = 'access_token'
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True,
                                       nullable=False,
                                       index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='access_token')
