import uuid
from dataclasses import dataclass


@dataclass
class TokenResultDTO:
    accessToken: str
    expiresIn: int
    refreshToken: uuid.UUID
    tokenType: str
