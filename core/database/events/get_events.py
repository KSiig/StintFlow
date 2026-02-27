"""
Get all events from the database.

Retrieves all race events stored in the MongoDB events collection.
Results are returned as a materialized list and can be optionally sorted.
"""

from pymongo.errors import PyMongoError
from core.errors import log, log_exception
from ..connection import get_events_collection


def get_events(sort_by: str = 'name', ascending: bool = False) -> list[dict]:
    """
    Retrieve all events from the database.
    
    Args:
        sort_by: Field to sort by ('tires', 'name', or None for no sorting).
                 Defaults to 'name' for alphabetical order.
        ascending: Sort order - True for ascending, False for descending.
                   Defaults to False (most recent first).
    
    Returns:
        List of event documents. Each document contains:
        - _id: ObjectId
        - name: str (event name)
        - tires: str (tire allocation count)
        - length: str (event duration in HH:MM:SS format)
        
    Raises:
        PyMongoError: If database query fails
        
    Example:
        >>> events = get_events()  # Get all events, newest first
        >>> events = get_events(sort_by='name', ascending=True)  # Alphabetical
    """
    try:
        events_col = get_events_collection()
        
        # Build query with optional sorting
        query = events_col.find()
        
        if sort_by:
            sort_direction = 1 if ascending else -1
            query = query.sort(sort_by, sort_direction)
        
        # Materialize cursor to list
        events = list(query)
        
        log('DEBUG', f'Retrieved {len(events)} events from database', 
            category='database', action='get_events')
        
        return events
        
    except PyMongoError as e:
        log_exception(e, 'Failed to retrieve events from database', 
                     category='database', action='get_events')
        raise
    except Exception as e:
        log_exception(e, 'Unexpected error retrieving events', 
                     category='database', action='get_events')
        raise
