"""
Tire calculation functions for table model.

Handles counting tire changes and recalculating remaining tires
based on tire data from stints.
"""

from core.database import get_event
from core.errors import log

from ..table_constants import TireData, ColumnIndex


def count_tire_changes(tire_data: TireData) -> tuple[int, int]:
    """
    Count tire changes and medium tire changes.
    
    Args:
        tire_data: Tire data dictionary from stint document
        
    Returns:
        Tuple of (total_tires_changed, medium_tires_changed)
    """
    total_changed = 0
    medium_changed = 0
    
    for tire in ["fl", "fr", "rl", "rr"]:
        is_changed = tire_data.get('tires_changed', {}).get(tire, False)
        compound = tire_data.get(tire, {}).get('outgoing', {}).get('compound', '').lower()
        
        if is_changed:
            total_changed += 1
            if compound == 'medium':
                medium_changed += 1
    
    return total_changed, medium_changed


def recalculate_tires_left(
    data: list[list],
    tires: list[dict],
    event_id: str,
    recalc_stint_types_fn
) -> None:
    """
    Recalculate remaining tires for all rows based on tire changes.
    
    Args:
        data: Table data array (will be modified)
        tires: Tire metadata array
        event_id: Event ID to get total tire count
        recalc_stint_types_fn: Function to recalculate stint types
    """
    event = get_event(event_id)
    if not event:
        log('WARNING', 'Cannot recalculate tires - event not found',
            category='table_model', action='recalc_tires')
        return
    
    tires_left = int(event.get('tires', 0))
    
    for i, row in enumerate(data):
        if i < len(tires):
            _, medium_changed = count_tire_changes(tires[i])
            tires_left -= medium_changed
        
        row[ColumnIndex.TIRES_LEFT] = str(tires_left)
    
    # Trigger stint type recalculation
    recalc_stint_types_fn()
