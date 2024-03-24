from collections.abc import Callable

from fastapi import Depends

from auth.common.application.protocols.password import PasswordProvider
from auth.common.presentation.dependencies.depends_stub import Stub

T = str | bytes
S = str | bytes | None


async def get_hashed_password(
        password_provider: PasswordProvider = Depends(Stub(PasswordProvider))
) -> Callable[[T], str]:
    return password_provider.get_password_hash


async def verify_hashed_password(
        password_provider: PasswordProvider = Depends()
) -> Callable[[T, S], bool]:
    return password_provider.verify_password
