from passlib.context import CryptContext

from auth.common.application.protocols.password import PasswordProvider


class PasswordCryptoProvider(PasswordProvider):
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def verify_password(
            self,
            secret: str | bytes,
            hash: str | bytes | None = None
    ) -> bool:
        return self.pwd_context.verify(secret, hash)

    def get_password_hash(self, secret: str | bytes) -> str:
        return self.pwd_context.hash(secret)
