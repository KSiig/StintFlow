"""
Update stint document in database.

Modifies tire data for a specific stint.
"""

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from .connection import get_stints_collection
from core.errors import log


def update_stint(stint_id: str, tire_data: dict) -> bool:
  """
  Update tire data for a stint.
    
  Args:
    stint_id: String representation of stint ObjectId
    tire_data: Tire data payload to store
        
  Returns:
    True if update successful, False otherwise
        
  Raises:
    ValueError: If stint_id is invalid or tire_data not provided
  """
  if not stint_id:
    raise ValueError("stint_id is required")

  if tire_data is None:
    raise ValueError("tire_data must be provided for update")

  try:
    stint_obj_id = ObjectId(stint_id)
    query = {"_id": stint_obj_id}
    update_doc = {"$set": {"tire_data": tire_data}}

    stints_col = get_stints_collection()
    result = stints_col.update_one(query, update_doc)

    if result.matched_count > 0:
      log('DEBUG', f'Updated stint tire data for {stint_id}',
        category='database', action='update_stint')
      return True

    log('WARNING', f'Stint {stint_id} not found',
      category='database', action='update_stint')
    return False

  except PyMongoError as e:
    log('ERROR', f'Database error updating stint {stint_id}: {e}',
      category='database', action='update_stint')
    return False
  except Exception as e:
    log('ERROR', f'Failed to update stint {stint_id}: {e}',
      category='database', action='update_stint')
    return False