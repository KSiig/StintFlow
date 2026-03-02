"""Register error handlers for event routing."""

from ._state import error_handlers


def register_error_handler(category: str, action: str, handler_function) -> None:
    """Register a handler function for a specific error event."""
    if category not in error_handlers:
        error_handlers[category] = {}
    error_handlers[category][action] = handler_function
