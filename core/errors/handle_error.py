"""
Central error handler that processes error events and determines recovery actions.

This module provides centralized error handling that reacts to error events
in the format used throughout the application. It determines appropriate
recovery actions and logs errors appropriately.
"""

from .log_error import log


# Registry of error handlers by category and action
_error_handlers = {}


def register_error_handler(category, action, handler_function):
    """
    Register a handler function for a specific error event.
    
    Args:
        category (str): The category/component (e.g., 'stint_tracker', 'database')
        action (str): The action/event (e.g., 'stint_created', 'connection_failed')
        handler_function (callable): Function to call when this error occurs
        
    Handlers should accept any additional keyword arguments that may be passed
    during error handling. They should return True if handled successfully,
    False otherwise.
    """
    if category not in _error_handlers:
        _error_handlers[category] = {}
    _error_handlers[category][action] = handler_function


def handle_error(event_string, **kwargs):
    """
    Process an error event string and route it to the appropriate handler.
    
    Args:
        event_string (str): Error event in format '__event__:category:action' 
                          or '__info__:category:action' or '__error__:category:action'
        **kwargs: Additional context to pass to the error handler
        
    Returns:
        bool: True if error was handled successfully, False otherwise
        
    The function parses the event string, logs it appropriately, and routes
    it to registered handlers. If no handler is registered, it logs the
    event and returns False (graceful degradation).
    
    Example:
        handle_error("__event__:stint_tracker:stint_created")
        handle_error("__error__:database:connection_failed", retry_count=3)
    """
    if not event_string or not event_string.startswith('__'):
        log('WARNING', f"Invalid error event format: {event_string}")
        return False
    
    # Parse event string: __prefix__:category:action
    parts = event_string.split(':')
    if len(parts) < 3:
        log('WARNING', f"Malformed error event: {event_string}")
        return False
    
    prefix = parts[0].strip()
    category = parts[1].strip()
    action = parts[2].strip()
    
    # Determine log level based on prefix
    if prefix == '__error__':
        log_level = 'ERROR'
    elif prefix == '__warning__':
        log_level = 'WARNING'
    elif prefix == '__info__':
        log_level = 'INFO'
    elif prefix == '__event__':
        log_level = 'INFO'
    elif prefix == '__debug__':
        log_level = 'DEBUG'
    else:
        log_level = 'INFO'
    
    # Log the event
    log(log_level, f"Event received: {action}", category=category, action=action)
    
    # Also print in the original format for backward compatibility
    print(event_string)
    
    # Route to registered handler if available
    if category in _error_handlers and action in _error_handlers[category]:
        try:
            handler = _error_handlers[category][action]
            result = handler(**kwargs)
            if result:
                log('DEBUG', f"Handler for {category}:{action} executed successfully")
            else:
                log('WARNING', f"Handler for {category}:{action} returned False")
            return result
        except Exception as e:
            # Fail silently - log the exception but don't crash
            log('ERROR', f"Error handler for {category}:{action} raised exception: {str(e)}")
            return False
    else:
        # No handler registered - this is okay, just log it
        log('DEBUG', f"No handler registered for {category}:{action}")
        return False
