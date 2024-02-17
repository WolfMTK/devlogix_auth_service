from pydantic import BaseModel


class TokenGet(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TokenUpdate(BaseModel):
    refresh_token: str
