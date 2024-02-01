from datetime import datetime, timedelta

import jwt

from app.core import settings


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({'exp': expire})
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode,
                      settings.secret_token.get_secret_value(),
                      algorithm=settings.algorithm)

def decode_token(token: str) -> dict:
    return jwt.decode(token,
                      settings.secret_token.get_secret_value(),
                      algorithms=[settings.algorithm])
