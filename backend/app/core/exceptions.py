from typing import Any, Optional

class ForecastIQException(Exception):
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500, details: Optional[Any] = None):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

class EntityNotFoundException(ForecastIQException):
    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            message=f"{entity_name} with id '{entity_id}' was not found.",
            code="ENTITY_NOT_FOUND",
            status_code=404
        )

class UnauthorizedException(ForecastIQException):
    def __init__(self, message: str = "Invalid authentication credentials"):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401
        )

class PermissionDeniedException(ForecastIQException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            message=message,
            code="PERMISSION_DENIED",
            status_code=403
        )

class BadRequestException(ForecastIQException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(
            message=message,
            code="BAD_REQUEST",
            status_code=400
        )
