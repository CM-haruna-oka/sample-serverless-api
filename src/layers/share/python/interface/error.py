import string


class LambdaException(Exception):
    def __init__(self, status_code, error_code, message):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message


class ValidationError(LambdaException):
    def __init__(self, message):
        super(
            ValidationError,
            self).__init__(
            status_code=422,
            error_code='ValidationError',
            message=message)


class EntityNotFound(LambdaException):
    def __init__(self, error_code, message):
        super(
            EntityNotFound,
            self).__init__(
            status_code=404,
            error_code=error_code,
            message=message)
