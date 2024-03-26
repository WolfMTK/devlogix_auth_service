import uuid

from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

from auth.common.adapters.database.models import Base
from auth.core.constants import EMAIL_LENGTH


class User(Base):
    __tablename__ = 'user'
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(nullable=False, index=True)
    email: Mapped[str] = mapped_column(nullable=False, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    token = relationship(
        'Token',
        back_populates='user',
        lazy='joined',
        uselist=False
    )

    @validates('email')
    def validate_email(self, _: str, email: str) -> str:
        if len(email) > EMAIL_LENGTH:
            raise ValueError('The allowed length for E-mail is exceeded.')
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            raise ValueError('The value for the email field is invalid.')
        return email
