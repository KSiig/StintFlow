"""Shared state for error handler registry."""

# category -> action -> handler
error_handlers: dict[str, dict[str, object]] = {}
