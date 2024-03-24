from dataclasses import dataclass

from auth.user.domain.models.user_id import UserID


@dataclass
class UserDTO:
    username: str
    email: str
    password: str


@dataclass
class UserMeDTO:
    username: str


@dataclass
class UserResultDTO:
    id: UserID
    email: str
    username: str
