"""
Update session document in database.

Modifies session name.
"""

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from ..connection import get_sessions_collection
from core.errors import log


def update_session(session_id: str, name: str = None) -> bool:
    """
    Update session details.
    
    Args:
        session_id: String representation of session ObjectId
        name: Session name (optional)
        
    Returns:
        True if update successful, False otherwise
        
    Raises:
        ValueError: If session_id is invalid or name not provided
    """
    if not session_id:
        raise ValueError("session_id is required")
    
    if name is None:
        raise ValueError("name must be provided for update")
    
    try:
        # Convert string ID to ObjectId
        session_obj_id = ObjectId(session_id)
        
        # Prepare query and update
        query = {"_id": session_obj_id}
        update_doc = {"$set": {"name": name}}
        
        # Update database
        sessions_col = get_sessions_collection()
        result = sessions_col.update_one(query, update_doc)
        
        if result.matched_count > 0:
            log('DEBUG', f'Updated session name: {name}',
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
