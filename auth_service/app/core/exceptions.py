class HTTPError404(BaseException):
    """Not Found"""


class HTTPError401(BaseException):
    """Unauthorized"""


class HTTPError400(BaseException):
    """Bad Request"""


class InvalidDataError(BaseException):
    """Invalid Data"""
