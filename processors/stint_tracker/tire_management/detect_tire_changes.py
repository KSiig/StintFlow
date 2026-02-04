"""
Detect which tires were changed during pit stop.

Compares incoming and outgoing tire states to identify changes.
"""

from .constants import TIRE_POSITIONS, NEW_TIRE_THRESHOLD


def detect_tire_changes(tires_outgoing: dict) -> dict:
    """
    Detect which tires were changed during the pit stop.
    
    A tire is considered changed if the outgoing wear is 1.00 or very close
    to 1.00 (brand new tire).
    
    Args:
        tires_outgoing: Tire state when leaving pits
        
    Returns:
        Dictionary indicating which tires were changed:
        {
            "fl": bool,
            "fr": bool,
            "rl": bool,
            "rr": bool
        }
    """
    tires_changed = {}
    
    for tire_pos in TIRE_POSITIONS:
        outgoing = tires_outgoing.get(tire_pos, {})
        outgoing_wear = outgoing.get("wear")
        
        # If wear data is missing, assume tire was not changed
        if outgoing_wear is None:
            tires_changed[tire_pos] = False
        else:
            # Tire is new if wear is >= threshold (accounts for float precision)
            tires_changed[tire_pos] = outgoing_wear >= NEW_TIRE_THRESHOLD
    
    return tires_changed
