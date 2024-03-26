from auth.user.application.protocols.gateway import (
    UserCreated,
    UserCheck,
    UserReading,
)


class StubUserGateway(UserCreated, UserCheck, UserReading):
    pass
