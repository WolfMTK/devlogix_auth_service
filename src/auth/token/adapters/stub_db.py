from auth.token.application.protocols.gateway import TokenCreated
from auth.user.application.protocols.gateway import UserCheck, UserReading


class StubTokenGateway(TokenCreated, UserCheck, UserReading):
    pass
