"""Load events from database into the events combo box."""

from pymongo.errors import PyMongoError

from core.database import get_events
from core.errors import log, log_exception


def _load_events(self) -> None:
    """Clear and load all events into the events combo box."""
    try:
        events = get_events(sort_by=None)
        for doc in events:
            self.events.addItem(doc["name"], userData=str(doc["_id"]))
        log('DEBUG', f'Loaded {len(events)} events into combo box', category='ui', action='load_events')
    except PyMongoError as exc:
        log_exception(exc, 'Failed to load events from database', category='ui', action='load_events')
    except Exception as exc:
        log_exception(exc, 'Unexpected error loading events', category='ui', action='load_events')
