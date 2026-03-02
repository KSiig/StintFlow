"""Public log entrypoint."""

import logging

from .helpers._configure_logger import _configure_logger


def log(level: str, message: str, category: str | None = None, action: str | None = None) -> None:
    """Log a message to both console and file."""
    _configure_logger()
    logger = logging.getLogger("stintflow")

    if category and action:
        formatted_message = f"[{category}:{action}] {message}"
    elif category:
        formatted_message = f"[{category}] {message}"
    else:
        formatted_message = message

    level_upper = level.upper()
    if level_upper == "DEBUG":
        logger.debug(formatted_message)
    elif level_upper == "INFO":
        logger.info(formatted_message)
    elif level_upper == "WARNING":
        logger.warning(formatted_message)
    elif level_upper == "ERROR":
        logger.error(formatted_message)
    elif level_upper == "CRITICAL":
        logger.critical(formatted_message)
    else:
        logger.info(formatted_message)
