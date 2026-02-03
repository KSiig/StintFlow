"""
Update driver names in team document.

Modifies the drivers field for the team.
"""

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from .connection import get_teams_collection
from core.errors import log


def update_team_drivers(team_id: str, drivers: list) -> bool:
    """
    Update the list of drivers for a team.
    
    Args:
        team_id: String representation of team ObjectId
        drivers: List of driver names as strings
        
    Returns:
        True if update successful, False otherwise
        
    Raises:
        ValueError: If team_id or drivers is invalid
    """
    if not team_id:
        raise ValueError("team_id is required")
    
    if not isinstance(drivers, list):
        raise ValueError("drivers must be a list")
    
    try:
        # Convert string ID to ObjectId
        team_obj_id = ObjectId(team_id)
        
        # Prepare update document
        query = {"_id": team_obj_id}
        update_doc = {"$set": {"drivers": drivers}}
        
        # Update database
        teams_col = get_teams_collection()
        result = teams_col.update_one(query, update_doc)
        
        if result.matched_count > 0:
            log('DEBUG', f'Updated team drivers: {len(drivers)} drivers',
                category='database', action='update_team_drivers')
            return True
        else:
            log('WARNING', f'Team {team_id} not found',
                category='database', action='update_team_drivers')
            return False
        
    except PyMongoError as e:
        log('ERROR', f'Database error updating team {team_id}: {e}',
            category='database', action='update_team_drivers')
        return False
    except Exception as e:
        log('ERROR', f'Failed to update team {team_id}: {e}',
            category='database', action='update_team_drivers')
        return False
