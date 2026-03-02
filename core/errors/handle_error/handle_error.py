"""Central error handler that processes error events and determines recovery actions."""

from core.errors.log_error import log
from ._state import error_handlers


def handle_error(event_string: str, **kwargs) -> bool:
    """Process an error event string and route it to the appropriate handler."""
    if not event_string or not event_string.startswith("__"):
        log("WARNING", f"Invalid error event format: {event_string}")
        return False

    parts = event_string.split(":", 2)
    if len(parts) < 3:
        log("WARNING", f"Malformed error event: {event_string}")
        return False

    prefix = parts[0].strip()
    category = parts[1].strip()
    action = parts[2].strip()

    if prefix == "__error__":
        log_level = "ERROR"
    elif prefix == "__warning__":
        log_level = "WARNING"
    elif prefix in {"__info__", "__event__"}:
        log_level = "INFO"
    elif prefix == "__debug__":
        log_level = "DEBUG"
    else:
        log_level = "INFO"

    log(log_level, f"Event received: {action}", category=category, action=action)
    print(event_string)

    if category in error_handlers and action in error_handlers[category]:
        try:
            handler = error_handlers[category][action]
            result = handler(**kwargs)
            if result:
                log("DEBUG", f"Handler for {category}:{action} executed successfully")
            else:
                log("WARNING", f"Handler for {category}:{action} returned False")
            return bool(result)
        except Exception as exc:  # fail gracefully
            log("ERROR", f"Error handler for {category}:{action} raised exception: {exc}")
            return False

    log("DEBUG", f"No handler registered for {category}:{action}")
    return False
