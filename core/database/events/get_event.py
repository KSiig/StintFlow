"""
Retrieve event from database.

Query function for loading a single event by ID.
"""

from bson.objectid import ObjectId

from ..connection import get_events_collection
from core.errors import log


def get_event(event_id: str) -> dict:
    """
    Retrieve a single event by ID.
    
    Args:
        event_id: String representation of event ObjectId
        
    Returns:
        Event document with name, tires, length fields
        None if event not found or on error
        
    Raises:
        ValueError: If event_id is invalid
    """
    if not event_id:
        raise ValueError("event_id is required")
    
    try:
        # Convert string ID to ObjectId
        event_obj_id = ObjectId(event_id)
        
        # Query database
        events_col = get_events_collection()
        event = events_col.find_one({"_id": event_obj_id})
        
        if event:
            log('DEBUG', f'Retrieved event: {event.get("name")}',
                category='database', action='get_event')
        else:
            log('WARNING', f'Event not found: {event_id}',
                category='database', action='get_event')
        
        return event
        
    except Exception as e:
        log('ERROR', f'Failed to retrieve event {event_id}: {e}',
            category='database', action='get_event')
        return None
