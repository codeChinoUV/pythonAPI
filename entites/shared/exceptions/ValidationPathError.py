from typing import Any


class ValidationPathError(Exception):
    """
    Represent a validation error in the path field
    """
    message: str
    field: str
    value: Any

    def __init__(self, message: str, field: str, value):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(message)
