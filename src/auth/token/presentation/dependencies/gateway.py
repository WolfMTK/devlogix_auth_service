from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.common.presentation.dependencies.depends_stub import Stub
from auth.token.adapters.database.gateway import TokenGateway
from auth.token.adapters.stub_db import StubTokenGateway


async def new_token_gateway(
        session: AsyncSession = Depends(Stub(AsyncSession))
) -> AsyncIterator[StubTokenGateway]:
    yield TokenGateway(session)
