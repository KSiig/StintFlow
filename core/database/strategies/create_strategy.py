"""
Create a new strategy in the database.

Inserts a strategy document into the strategies collection.
"""

from bson import ObjectId
from ..connection import get_strategies_collection


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
    coll = get_strategies_collection()
    result = coll.insert_one(strategy)
    return result.inserted_id
