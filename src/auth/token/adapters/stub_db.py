from auth.token.application.protocols.gateway import TokenCreated
from auth.user.application.protocols.gateway import UserCheck


class StubTokenGateway(TokenCreated, UserCheck):
    pass
