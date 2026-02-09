"""
Centralized error handling and logging module.

This module provides a unified error handling system that:
- Logs errors to both console and file with appropriate log levels
- Routes error events to registered handlers
- Fails gracefully without crashing the application
- Provides user-accessible log files for debugging

Usage:
    from core.errors import handle_error, log, log_exception, register_error_handler
    
    # Log a message
    log('ERROR', 'Something went wrong', category='database', action='connection_failed')
    
    # Log an exception with traceback
    try:
        # some code
        pass
    except Exception as e:
        log_exception(e, 'Failed to connect', category='database', action='connection_failed')
    
    # Handle an error event
    handle_error('__event__:stint_tracker:stint_created')
    
    # Register a custom handler
    def my_handler(**kwargs):
        # Handle the error
        return True
    
    register_error_handler('stint_tracker', 'stint_created', my_handler)
"""

from .handle_error import handle_error, register_error_handler
from .log_error import log, log_exception
from .get_log_file_path import get_log_file_path

__all__ = ['handle_error', 'register_error_handler', 'log', 'log_exception', 'get_log_file_path']
