"""
Retrieve team from database.

Query function for loading team data including driver names.
"""

from pymongo.errors import PyMongoError

from ..connection import get_teams_collection
from core.errors import log


def get_team() -> dict:
    """
    Retrieve the team document (assumes single team in database).
    
    Returns:
        Team document with drivers field (list of driver names)
        None if team not found or on error
    """
    try:
        # Query database - assumes one team per database
        teams_col = get_teams_collection()
        team = teams_col.find_one()
        
        if team:
            log('DEBUG', f'Retrieved team with {len(team.get("drivers", []))} drivers',
                category='database', action='get_team')
        else:
            log('WARNING', 'No team found in database',
                category='database', action='get_team')
        
        return team
        
    except PyMongoError as e:
        log('ERROR', f'Database error retrieving team: {e}',
            category='database', action='get_team')
        return None
    except Exception as e:
        log('ERROR', f'Failed to retrieve team: {e}',
            category='database', action='get_team')
        return None
