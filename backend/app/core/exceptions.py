"""
Custom exception hierarchy for the application.

Each exception maps to an HTTP status code so the global
exception handler in main.py can translate them automatically.
"""

from __future__ import annotations


class AppError(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str = "An unexpected error occurred", status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Resource", identifier: str = "") -> None:
        detail = f"{resource} not found"
        if identifier:
            detail = f"{resource} with id '{identifier}' not found"
        super().__init__(message=detail, status_code=404)


class ValidationError(AppError):
    """Raised when input data fails business-rule validation."""

    def __init__(self, message: str = "Validation failed") -> None:
        super().__init__(message=message, status_code=422)


class LLMError(AppError):
    """Raised when the LLM provider (Groq) returns an error."""

    def __init__(self, message: str = "LLM service unavailable") -> None:
        super().__init__(message=message, status_code=502)


class DatabaseError(AppError):
    """Raised when a database operation fails unexpectedly."""

    def __init__(self, message: str = "Database operation failed") -> None:
        super().__init__(message=message, status_code=500)
