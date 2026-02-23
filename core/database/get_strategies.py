"""
Get all strategies for a session.

Retrieves strategy documents from the strategies collection.
"""

from bson import ObjectId
from .connection import get_strategies_collection


def get_strategies(session_id: str):
    """
    Get all strategies for a specific session.
    
    Args:
        session_id: Session ID as string
        
    Returns:
        Cursor of strategy documents
    """
    coll = get_strategies_collection()
    return coll.find({"session_id": ObjectId(session_id)})
