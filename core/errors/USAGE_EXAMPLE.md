# Error Handling Module Usage

This module provides centralized error handling and logging for StintFlow.

## Basic Usage

### Logging Messages

```python
from core.errors import log

# Log at different levels
log('DEBUG', 'Detailed debugging information')
log('INFO', 'General information message')
log('WARNING', 'Something might be wrong')
log('ERROR', 'An error occurred', category='database', action='connection_failed')
log('CRITICAL', 'Critical failure that may cause crash')
```

### Handling Error Events

```python
from core.errors import handle_error

# Handle events in the existing format
handle_error("__event__:stint_tracker:stint_created")
handle_error("__info__:stint_tracker:return_to_garage")
handle_error("__error__:database:connection_failed")
```

### Registering Custom Handlers

```python
from core.errors import register_error_handler, handle_error

def on_stint_created(**kwargs):
    """Handle when a stint is created."""
    # Your logic here
    print("Stint was created!")
    return True  # Return True if handled successfully

# Register the handler
register_error_handler('stint_tracker', 'stint_created', on_stint_created)

# Now when this event occurs, your handler will be called
handle_error("__event__:stint_tracker:stint_created")
```

### Logging Exceptions with Stack Traces

```python
from core.errors import log_exception

# Catch exceptions and log them with full stack traces
try:
    # Some operation that might fail
    result = risky_operation()
    process_data(result)
except ValueError as e:
    # Log the exception with full stack trace
    log_exception(e, "Failed to process data", category='data_processing', action='parse')
    # Application continues gracefully - no crash
except ConnectionError as e:
    log_exception(e, "Database connection failed", category='database', action='connect')
    # Fallback to cached data or show user-friendly message
except Exception as e:
    # Catch-all for unexpected errors
    log_exception(e, "Unexpected error occurred", category='system', action='unknown')
    # Application degrades gracefully
```

**Important**: The `log_exception()` function automatically includes the full stack trace in both:
- **Console output**: Shows the error and traceback for immediate debugging
- **Log file**: Complete traceback is written for later analysis

The stack trace includes:
- The exception type and message
- The full call stack showing where the error occurred
- Line numbers and file names for each frame
- All context needed for debugging

### Getting Log File Location

```python
from core.errors import get_log_file_path

log_path = get_log_file_path()
print(f"Log file is at: {log_path}")
# Example: C:\Users\Username\StintFlow\stintflow.log
```

## Migration from Old Code

Replace direct `print()` statements:

**Old:**
```python
print("__event__:stint_tracker:stint_created")
```

**New:**
```python
from core.errors import handle_error
handle_error("__event__:stint_tracker:stint_created")
```

Or if you just need logging without event handling:

```python
from core.errors import log
log('INFO', 'Stint created', category='stint_tracker', action='stint_created')
```

## Complete Exception Handling Example

Here's a complete example showing proper exception handling with stack traces:

```python
from core.errors import log_exception, log

def process_stint_data(data):
    """Process stint data with proper error handling."""
    try:
        # Validate input
        if not data:
            raise ValueError("Data cannot be empty")
        
        # Process the data
        result = complex_processing_function(data)
        
        log('INFO', 'Stint data processed successfully', 
            category='stint_tracker', action='process')
        return result
        
    except ValueError as e:
        # Log validation errors with stack trace
        log_exception(e, "Invalid input data", 
                     category='stint_tracker', action='validate')
        return None  # Graceful degradation
        
    except KeyError as e:
        # Log missing key errors
        log_exception(e, "Required data field missing", 
                     category='stint_tracker', action='process')
        return None
        
    except Exception as e:
        # Catch-all for unexpected errors
        log_exception(e, "Unexpected error processing stint data", 
                     category='stint_tracker', action='process')
        return None  # Application continues, doesn't crash
```

**Key Points:**
- Always catch specific exceptions first, then general `Exception` as fallback
- Use `log_exception()` to ensure full stack traces are captured
- Return sensible defaults or None to allow graceful degradation
- Never let exceptions crash the application - always catch and log them

## Log File Location

Logs are written to: `%USERPROFILE%\StintFlow\stintflow.log` (Windows) or `~/StintFlow/stintflow.log` (Unix)

This location is user-accessible so non-technical users can easily find and send log files for debugging.

**Stack traces in log files**: When exceptions are logged using `log_exception()`, the complete stack trace is written to the log file, making it easy to debug issues even when you can't reproduce them locally.
