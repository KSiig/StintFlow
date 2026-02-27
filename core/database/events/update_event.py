"""
Update event document in database.

Modifies event name, tire count, and race length.
"""

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from ..connection import get_events_collection
from core.errors import log


def update_event(event_id: str, name: str = None, tires: str = None, length: str = None, start_time: str = None) -> bool:
    """
    Update event details.
    
    Args:
        event_id: String representation of event ObjectId
        name: Event name (optional)
        tires: Starting tire count as string (optional)
        length: Race length in HH:MM:SS format (optional)
        start_time: Start time in HH:MM:SS format (optional)
    Returns:
        True if update successful, False otherwise
        
    Raises:
        ValueError: If event_id is invalid or no update fields provided
    """
    if not event_id:
        raise ValueError("event_id is required")
    
    # Build update document only with provided fields
    update_fields = {}
    if name is not None:
        update_fields['name'] = name
    if tires is not None:
        update_fields['tires'] = tires
    if length is not None:
        update_fields['length'] = length
    if start_time is not None:
        update_fields['start_time'] = start_time
    if not update_fields:
        raise ValueError("At least one field must be provided for update")
    
    try:
        # Convert string ID to ObjectId
        event_obj_id = ObjectId(event_id)
        
        # Prepare query and update
        query = {"_id": event_obj_id}
        update_doc = {"$set": update_fields}
        
        # Update database
        events_col = get_events_collection()
        result = events_col.update_one(query, update_doc)
        
        if result.matched_count > 0:
            log('DEBUG', f'Updated event: {update_fields}',
                category='database', action='update_event')
            return True
        else:
            log('WARNING', f'Event {event_id} not found',
                category='database', action='update_event')
            return False
        
    except PyMongoError as e:
        log('ERROR', f'Database error updating event {event_id}: {e}',
            category='database', action='update_event')
        return False
    except Exception as e:
        log('ERROR', f'Failed to update event {event_id}: {e}',
            category='database', action='update_event')
        return False
