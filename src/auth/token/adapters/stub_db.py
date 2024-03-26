from auth.token.application.protocols.gateway import (
    TokenCreated,
    TokenDeleted,
)
from auth.user.application.protocols.gateway import UserCheck, UserReading


class StubTokenGateway(TokenCreated, UserCheck, UserReading, TokenDeleted):
    pass
