"""
Update session document in database.

Modifies session name.
"""

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from ..connection import get_sessions_collection
from core.errors import log


def update_session(session_id: str, name: str = None, tires_remaining_at_green_flag: int = None) -> bool:
    """
    Update session details.
    
    Args:
        session_id: String representation of session ObjectId
        name: Session name (optional)
        tires_remaining_at_green_flag: Tires remaining at green flag (optional)
        
    Returns:
        True if update successful, False otherwise
        
    Raises:
        ValueError: If session_id is invalid or neither name nor tires_remaining_at_green_flag is provided
    """
    if not session_id:
        raise ValueError("session_id is required")
    
    if name is None and tires_remaining_at_green_flag is None:
        raise ValueError("At least one of name or tires_remaining_at_green_flag must be provided for update")
    
    try:
        # Convert string ID to ObjectId
        session_obj_id = ObjectId(session_id)
        
        # Prepare query and update
        query = {"_id": session_obj_id}
        update_doc = {"$set": {}}
        if name is not None:
            update_doc["$set"]["name"] = name
        if tires_remaining_at_green_flag is not None:
            update_doc["$set"]["tires_remaining_at_green_flag"] = tires_remaining_at_green_flag
        
        # Update database
        sessions_col = get_sessions_collection()
        result = sessions_col.update_one(query, update_doc)
        
        if result.matched_count > 0:
            log('DEBUG', f'Updated session name: {name}, tires_remaining_at_green_flag: {tires_remaining_at_green_flag}',
                category='database', action='update_session')
            return True
        else:
            log('WARNING', f'Session {session_id} not found',
                category='database', action='update_session')
            return False
        
    except PyMongoError as e:
        log('ERROR', f'Database error updating session {session_id}: {e}',
            category='database', action='update_session')
        return False
    except Exception as e:
        log('ERROR', f'Failed to update session {session_id}: {e}',
            category='database', action='update_session')
        return False
