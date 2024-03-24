from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.common.presentation.dependencies.depends_stub import Stub
from auth.user.adapters.database.gateway import UserGateway
from auth.user.adapters.stub_db import StubUserGateway


async def new_user_gateway(
        session: AsyncSession = Depends(Stub(AsyncSession))
) -> AsyncIterator[StubUserGateway]:
    yield UserGateway(session)
