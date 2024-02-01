class InvalidNameTaskError(Exception):
    def __init__(self,
                 message: str = 'Некорректное название задачи'):
        super().__init__(message)
