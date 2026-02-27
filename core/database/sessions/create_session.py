"""
Create a new session in database.

Inserts session document with race_id and name.
"""

from pymongo.errors import PyMongoError
from pymongo.results import InsertOneResult

from ..connection import get_sessions_collection
from core.errors import log


def create_session(session_data: dict) -> InsertOneResult:
    """
    Create a new session.
    
    Args:
        session_data: Dictionary containing session fields (race_id, name)
        
    Returns:
        InsertOneResult with inserted_id field
        None on error
        
    Raises:
        ValueError: If session_data is invalid
    """
    if not session_data or not isinstance(session_data, dict):
        raise ValueError("session_data must be a non-empty dictionary")
    
    try:
        # Insert into database
        sessions_col = get_sessions_collection()
        result = sessions_col.insert_one(session_data)
        
        log('DEBUG', f'Created session: {session_data.get("name")}',
            category='database', action='create_session')
        
        return result
        
    except PyMongoError as e:
        log('ERROR', f'Database error creating session: {e}',
            category='database', action='create_session')
        return None
    except Exception as e:
        log('ERROR', f'Failed to create session: {e}',
            category='database', action='create_session')
        return None
