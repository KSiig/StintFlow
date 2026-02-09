"""
Create a new strategy in the database.

Inserts a strategy document into the strategies collection.
"""

from bson import ObjectId
from .connection import strategies_col


def create_strategy(strategy: dict) -> ObjectId:
    """
    Create a new race strategy in the database.
    
    Args:
        strategy: Strategy document with structure:
            {
                'session_id': ObjectId,
                'name': str,
                'model_data': {
                    'rows': [...],
                    'tires': [...]
                }
            }
    
    Returns:
        ObjectId of the inserted strategy document
    """
    result = strategies_col.insert_one(strategy)
    return result.inserted_id
