"""Populate the sessions combo box for a specific event."""

from pymongo.errors import PyMongoError

from core.database import get_sessions
from core.errors import log, log_exception


def _populate_sessions(self, event_id: str = None) -> None:
    """Populate sessions for the provided event id."""
    self.sessions.blockSignals(True)
    self.sessions.clear()

    if not event_id:
        self.sessions.blockSignals(False)
        return

    try:
        sessions = get_sessions(event_id, sort_by=None)
        for doc in sessions:
            self.sessions.addItem(doc["name"], userData=str(doc["_id"]))
        log('DEBUG', f'Loaded {len(sessions)} sessions for event {event_id}', category='ui', action='populate_sessions')
    except ValueError as exc:
        log_exception(exc, f'Invalid event ID: {event_id}', category='ui', action='populate_sessions')
    except PyMongoError as exc:
        log_exception(exc, f'Failed to load sessions for event {event_id}', category='ui', action='populate_sessions')
    except Exception as exc:
        log_exception(exc, f'Unexpected error loading sessions for event {event_id}', category='ui', action='populate_sessions')
    finally:
        self.sessions.blockSignals(False)
