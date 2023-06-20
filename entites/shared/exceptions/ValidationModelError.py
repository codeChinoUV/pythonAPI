from typing import Any


class ValidationModelError(Exception):
    """
    Custom exception for validations on use cases
    """
    field: str
    message: str
    value: any

    def __init__(self, field: str, message: str, value: Any):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)
