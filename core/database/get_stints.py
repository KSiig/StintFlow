"""
Retrieve stints from database.

Query function for loading stint data for a specific session.
"""

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from .connection import get_stints_collection
from core.errors import log


def get_stints(session_id: str) -> list[dict]:
    """
    Retrieve all stints for a specific session.
    
    Args:
        session_id: String representation of session ObjectId
        
    Returns:
        List of stint documents with tire data, pit times, driver info
        Empty list if no stints found or on error
        
    Raises:
        ValueError: If session_id is invalid
    """
    if not session_id:
        raise ValueError("session_id is required")
    
    try:
        # Convert string ID to ObjectId
        session_obj_id = ObjectId(session_id)
        
        # Query database
        stints_col = get_stints_collection()
        cursor = stints_col.find({"session_id": session_obj_id})
        
        # Materialize results
        stints = list(cursor)
        
        log('DEBUG', f'Retrieved {len(stints)} stints for session {session_id}',
            category='database', action='get_stints')
        
        return stints
        
    except Exception as e:
        log('ERROR', f'Failed to retrieve stints for session {session_id}: {e}',
            category='database', action='get_stints')
        return []
