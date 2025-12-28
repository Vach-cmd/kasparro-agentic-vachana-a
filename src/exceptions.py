"""
Custom exceptions for better error handling across the system.
"""


class ContentGenerationError(Exception):
    """Base exception for content generation errors"""
    pass


class DataValidationError(ContentGenerationError):
    """Raised when input data validation fails"""
    pass


class AgentExecutionError(ContentGenerationError):
    """Raised when an agent fails to execute properly"""
    pass


class TemplateRenderError(ContentGenerationError):
    """Raised when template rendering fails"""
    pass


class ContentBlockError(ContentGenerationError):
    """Raised when a content block fails to generate"""
    pass


class OutputGenerationError(ContentGenerationError):
    """Raised when output file generation fails"""
    pass
