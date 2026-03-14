"""Store the race-start tyre inventory for the tracked session."""

from __future__ import annotations

from core.database import set_tires_remaining_at_green_flag
from core.errors import log
from ..tire_management import _get_tire_management_data


def _store_tires_remaining_at_green_flag(session_id: str) -> bool:
    """Read LMU tyre inventory and persist the green-flag tyre count once.

    Returns True if the value was persisted successfully, False otherwise.
    """
    tire_management_data = _get_tire_management_data()
    if not isinstance(tire_management_data, dict):
        log(
            'WARNING',
            'Could not store green-flag tire snapshot because tire management data is unavailable',
            category='stint_tracker',
            action='store_tires_remaining_at_green_flag',
        )
        return False

    tire_inventory = tire_management_data.get('tireInventory')
    if not isinstance(tire_inventory, dict):
        log(
            'WARNING',
            'Could not store green-flag tire snapshot because tireInventory is missing',
            category='stint_tracker',
            action='store_tires_remaining_at_green_flag',
        )
        return False

    new_tires = tire_inventory.get('newTires')
    if isinstance(new_tires, bool) or not isinstance(new_tires, int):
        log(
            'WARNING',
            f'Could not store green-flag tire snapshot because newTires is invalid: {new_tires}',
            category='stint_tracker',
            action='store_tires_remaining_at_green_flag',
        )
        return False

    if new_tires < 0:
        log(
            'WARNING',
            f'Could not store green-flag tire snapshot because newTires is negative: {new_tires}',
            category='stint_tracker',
            action='store_tires_remaining_at_green_flag',
        )
        return False

    success = set_tires_remaining_at_green_flag(session_id, new_tires)
    if not success:
        log(
            'WARNING',
            f'Failed to persist green-flag tire count for session {session_id}',
            category='stint_tracker',
            action='store_tires_remaining_at_green_flag',
        )
    return success
