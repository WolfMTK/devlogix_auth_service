from typing import Any

import jwt

from auth.common.application.protocols.jwt import TokenProvider


class JWTProvider(TokenProvider):
    def __init__(self, secret_token: str, algorithm: str) -> None:
        self.secret_token = secret_token
        self.algorithm = algorithm

    def create_token(self, data: dict[str, Any]) -> str:
        to_encode = data.copy()
        return jwt.encode(
            payload=to_encode,
            key=self.secret_token,
            algorithm=self.algorithm
        )

    def decode_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(
            jwt=token,
            key=self.secret_token,
            algorithms=[self.algorithm]
        )
