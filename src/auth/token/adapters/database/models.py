import datetime as dt
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from auth.common.adapters.database.models import Base


class Token(Base):
    __tablename__ = "token"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now())
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'),nullable=False)
    user = relationship('User', back_populates='token')
