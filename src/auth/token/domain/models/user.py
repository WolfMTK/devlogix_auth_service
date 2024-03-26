from dataclasses import dataclass


@dataclass
class UserDTO:
    password: str
    username: str | None = None
    email: str | None = None
