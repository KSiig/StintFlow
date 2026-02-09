"""
Get sessions for a specific event from the database.

Retrieves all sessions associated with a given race event.
Results are returned as a materialized list and can be optionally sorted.
"""

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from core.errors import log, log_exception
from .connection import get_sessions_collection


def get_sessions(event_id: str, sort_by: str = "name", ascending: bool = True) -> list[dict]:
    """
    Retrieve all sessions for a specific event.
    
    Args:
        event_id: The event ID to get sessions for
        sort_by: Field to sort by (e.g., 'name', 'created_at', or None for no sorting).
                 Defaults to "name".
        ascending: Sort order - True for ascending, False for descending.
                   Defaults to True.
    
    Returns:
        List of session documents for the event. Each document contains:
        - _id: ObjectId
        - race_id: ObjectId (reference to event)
        - name: str (session name, e.g., 'practice', 'qualifying', 'race')
        
    Raises:
        PyMongoError: If database query fails
        ValueError: If event_id is not a valid ObjectId
        
    Example:
        >>> sessions = get_sessions("507f1f77bcf86cd799439011")
        >>> sessions = get_sessions(event_id, sort_by='name')
    """
    try:
        # Validate ObjectId format
        try:
            event_object_id = ObjectId(event_id)
        except Exception:
            raise ValueError(f'Invalid event ID format: {event_id}')
        
        sessions_col = get_sessions_collection()
        
        # Build query with optional sorting
        query = sessions_col.find({"race_id": event_object_id})
        
        if sort_by:
            sort_direction = 1 if ascending else -1
            query = query.sort(sort_by, sort_direction)
        
        # Materialize cursor to list
        sessions = list(query)
        
        log('DEBUG', f'Retrieved {len(sessions)} sessions for event {event_id}', 
            category='database', action='get_sessions')
        
        return sessions
        
    except ValueError:
        # Re-raise validation errors
        raise
    except PyMongoError as e:
        log_exception(e, f'Failed to retrieve sessions for event {event_id}', 
                     category='database', action='get_sessions')
        raise
    except Exception as e:
        log_exception(e, f'Unexpected error retrieving sessions for event {event_id}', 
                     category='database', action='get_sessions')
        raise
