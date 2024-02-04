from datetime import datetime, timedelta

import jwt

from auth.core import Settings


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({'exp': expire})
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode,
                      Settings.secret_token,
                      algorithm=Settings.algorithm)


def decode_token(token: str) -> dict:
    return jwt.decode(token,
                      Settings.secret_token,
                      algorithms=[Settings.algorithm])
