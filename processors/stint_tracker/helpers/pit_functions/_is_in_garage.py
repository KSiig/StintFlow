"""Helpers for determining pit/garage state from LMU scoring objects.

This module provides a small, defensive helper that reads the
`mInGarageStall` flag from an LMU player scoring object and returns a
boolean. It tolerates missing or malformed input and logs unexpected
conditions instead of raising.
"""

from typing import Any

from core.errors import log

from .PitState import PitState


def _is_in_garage(player_scoring: Any) -> bool:
    """Return True when `player_scoring` indicates the player is in garage.

    The function is defensive: if the expected attribute is missing or
    cannot be interpreted as an integer, it logs and returns ``False``.

    Args:
        player_scoring: LMU player vehicle scoring object (or similar).

    Returns:
        ``True`` if the scoring object indicates the garage stall state,
        otherwise ``False``.
    """
    val = getattr(player_scoring, "mInGarageStall", None)
    if val is None:
        log(
            "DEBUG",
            "player_scoring missing mInGarageStall attribute",
            category="stint_tracker",
            action="is_in_garage",
        )
        return False

    try:
        return int(val) == PitState.IN_GARAGE
    except Exception as exc:  # pragma: no cover - defensive logging
        log(
            "WARNING",
            f"Failed to evaluate garage state: {exc}",
            category="stint_tracker",
            action="is_in_garage",
        )
        return False