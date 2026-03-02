"""
Create a new event in database.

Inserts event document with name, tires, and length.
"""

from pymongo.errors import PyMongoError
from pymongo.results import InsertOneResult

from ..connection import get_events_collection
from core.errors import log


def create_event(event_data: dict) -> InsertOneResult:
    """
    Create a new event.
    
    Args:
        event_data: Dictionary containing event fields (name, tires, length)
        
    Returns:
        InsertOneResult with inserted_id field
        None on error
        
    Raises:
        ValueError: If event_data is invalid
    """
    if not event_data or not isinstance(event_data, dict):
        raise ValueError("event_data must be a non-empty dictionary")
    
    try:
        # Insert into database
        events_col = get_events_collection()
        result = events_col.insert_one(event_data)
        
        log('DEBUG', f'Created event: {event_data.get("name")}',
            category='database', action='create_event')
        
        return result
        
    except PyMongoError as e:
        log('ERROR', f'Database error creating event: {e}',
            category='database', action='create_event')
        return None
    except Exception as e:
        log('ERROR', f'Failed to create event: {e}',
            category='database', action='create_event')
        return None
