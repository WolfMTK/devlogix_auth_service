from dataclasses import dataclass

from auth.user.domain.models.user_id import UserID


@dataclass
class UserBase:
    username: str


@dataclass
class UserCreate(UserBase):
    email: str
    password: str


@dataclass
class UserMe(UserBase):
    pass


@dataclass
class UserResult(UserBase):
    id: UserID
    email: str


@dataclass
class UserUpdate:
    email: str | None = None
    username: str | None = None
    password: str | None = None
