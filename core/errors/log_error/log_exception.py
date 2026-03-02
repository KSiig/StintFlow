"""Log an exception with traceback."""

import logging

from .helpers._configure_logger import _configure_logger


def log_exception(
    exception: Exception,
    message: str | None = None,
    category: str | None = None,
    action: str | None = None,
) -> None:
    """Log an exception with full stack trace to both console and file."""
    _configure_logger()
    logger = logging.getLogger("stintflow")

    if message:
        if category and action:
            formatted_message = f"[{category}:{action}] {message}"
        elif category:
            formatted_message = f"[{category}] {message}"
        else:
            formatted_message = message
    else:
        if category and action:
            formatted_message = f"[{category}:{action}] Exception occurred"
        elif category:
            formatted_message = f"[{category}] Exception occurred"
        else:
            formatted_message = "Exception occurred"

    logger.exception(formatted_message)
