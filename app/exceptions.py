"""Custom exceptions for data standardization application."""


class DataStandardizationException(Exception):
    """Base exception for data standardization errors."""
    pass


class ValidationError(DataStandardizationException):
    """Raised when data validation fails."""
    pass


class FormattingError(DataStandardizationException):
    """Raised when data formatting fails."""
    pass


class ProcessingError(DataStandardizationException):
    """Raised when general processing fails."""
    pass


class LLMError(DataStandardizationException):
    """Raised when LLM operation fails."""
    pass
