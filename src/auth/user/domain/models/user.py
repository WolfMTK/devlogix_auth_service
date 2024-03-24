from dataclasses import dataclass, field

from email_validator import validate_email, EmailNotValidError

from auth.core.constants import EMAIL_LENGTH
from auth.user.domain.models.user_id import UserID


@dataclass
class User:
    id: UserID = field(init=False)
    email: str
    username: str
    password: str
    is_active: bool = field(init=False, default=True)

    def __post_init__(self):
        self.validate_email()

    def validate_email(self) -> None:
        if len(self.email) > EMAIL_LENGTH:
            raise ValueError('The allowed length for E-mail is exceeded.')

        try:
            validate_email(self.email, check_deliverability=False)
        except EmailNotValidError as error:
            raise ValueError('The value for the email field is invalid.')


@dataclass
class UserResult:
    id: UserID
    email: str
    username: str
