"""
Retrieve session from database.

Query function for loading a single session by ID.
"""

from bson.objectid import ObjectId

from ..connection import get_sessions_collection
from core.errors import log


def get_session(session_id: str) -> dict:
    """
    Retrieve a single session by ID.
    
    Args:
        session_id: String representation of session ObjectId
        
    Returns:
        Session document with name, race_id fields
        None if session not found or on error
        
    Raises:
        ValueError: If session_id is invalid
    """
    if not session_id:
        raise ValueError("session_id is required")
    
    try:
        # Convert string ID to ObjectId
        session_obj_id = ObjectId(session_id)
        
        # Query database
        sessions_col = get_sessions_collection()
        session = sessions_col.find_one({"_id": session_obj_id})
        
        if session:
            log('DEBUG', f'Retrieved session: {session.get("name")}',
                category='database', action='get_session')
        else:
            log('WARNING', f'Session not found: {session_id}',
                category='database', action='get_session')
        
        return session
        
    except Exception as e:
        log('ERROR', f'Failed to retrieve session {session_id}: {e}',
            category='database', action='get_session')
        return None
