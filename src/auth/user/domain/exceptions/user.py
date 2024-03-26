from auth.common.domain.exceptions.base import DomainError


class InvalidEmailException(DomainError):
    pass


class InvalidUsernameException(DomainError):
    pass


class EmptyUsernameException(DomainError):
    pass


class InactiveUserException(DomainError):
    pass
