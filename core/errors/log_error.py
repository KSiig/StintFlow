"""
Log error messages to both console and log file with appropriate log levels.

This module provides centralized logging functionality that writes to both
the console (for immediate feedback) and a log file (for user support).
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from .get_log_file_path import get_log_file_path


# Configure logging once when module is imported
_logger_configured = False


def _configure_logger():
    """
    Configure the Python logging system with file and console handlers.
    
    This sets up logging to write to both a file and console output,
    with appropriate formatting for each.
    """
    global _logger_configured
    
    if _logger_configured:
        return
    
    log_file = get_log_file_path()
    
    # Create logger
    logger = logging.getLogger('stintflow')
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers if module is reloaded
    if logger.handlers:
        return
    
    # File handler - detailed format with timestamp
    # Note: When log_exception() is used, Python's logging automatically appends
    # the full stack trace to the formatted message
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    # Console handler - simpler format
    # Note: Stack traces are automatically included when log_exception() is called
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Show DEBUG messages in console
    console_format = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_format)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    _logger_configured = True


def log(level, message, category=None, action=None):
    """
    Log a message at the specified level to both console and log file.
    
    Args:
        level (str): Log level - 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'
        message (str): The message to log
        category (str, optional): Category/component that generated the message
        action (str, optional): Action or event that occurred
        
    The message is formatted and written to both console output and the log file.
    For non-technical users, the log file location is easily accessible.
    """
    _configure_logger()
    logger = logging.getLogger('stintflow')
    
    # Format message with category and action if provided
    if category and action:
        formatted_message = f"[{category}:{action}] {message}"
    elif category:
        formatted_message = f"[{category}] {message}"
    else:
        formatted_message = message
    
    # Log at appropriate level
    level_upper = level.upper()
    if level_upper == 'DEBUG':
        logger.debug(formatted_message)
    elif level_upper == 'INFO':
        logger.info(formatted_message)
    elif level_upper == 'WARNING':
        logger.warning(formatted_message)
    elif level_upper == 'ERROR':
        logger.error(formatted_message)
    elif level_upper == 'CRITICAL':
        logger.critical(formatted_message)
    else:
        # Default to INFO if unknown level
        logger.info(formatted_message)


def log_exception(exception, message=None, category=None, action=None):
    """
    Log an exception with full stack trace to both console and log file.
    
    Args:
        exception (Exception): The exception object that was raised
        message (str, optional): Additional message to include with the exception
        category (str, optional): Category/component that generated the exception
        action (str, optional): Action or event that was being performed when exception occurred
        
    This function automatically includes the full stack trace in both console output
    and the log file. Use this when catching exceptions to ensure complete error
    information is captured for debugging.
    
    Example:
        try:
            risky_operation()
        except ValueError as e:
            log_exception(e, "Failed to process data", category='data_processing', action='parse')
    """
    _configure_logger()
    logger = logging.getLogger('stintflow')
    
    # Format message with category and action if provided
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
    
    # Use exception() method which automatically includes traceback
    logger.exception(formatted_message)
