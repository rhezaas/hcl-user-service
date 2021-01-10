class ErrorModel(Exception):
    code: int = None
    message: str = None
    detail: str = None

    def __init__(self, code: int, message: str, detail: str):
        super().__init__(message)
        self.code = code
        self.message = message
        self.detail = detail


class BadRequestException(ErrorModel):
    def __init__(self, detail: str = ''):
        super().__init__(400, 'Bad Request', detail)


class UnauthorizedException(ErrorModel):
    def __init__(self, detail: str = ''):
        super().__init__(401, 'Unauthorized', detail)


class NotFoundException(ErrorModel):
    def __init__(self, detail: str = ''):
        super().__init__(404, 'Not Found', detail)
