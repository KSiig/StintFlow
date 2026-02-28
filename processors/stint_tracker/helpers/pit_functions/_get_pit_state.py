"""
Pit state detection from LMU data.

Determines when player is pitting, entering/leaving pits, or in garage.
"""

"""Pit state detection helpers for LMU player scoring objects.

Expose a small, well-documented function that converts the raw
`mPitState` value from LMU into the `PitState` enum. The implementation
is defensive: missing or unexpected values are logged and the function
returns ``PitState.ON_TRACK`` as a safe default.
"""

from typing import Any

from core.errors import log

from .PitState import PitState


def _get_pit_state(player_scoring: Any) -> PitState:
    """Return the `PitState` for the given `player_scoring` object.

    Args:
        player_scoring: object from LMU shared memory exposing
            ``mPitState`` (or equivalent).

    Returns:
        A member of :class:`PitState`. Falls back to ``PitState.ON_TRACK``
        when the attribute is missing or cannot be parsed.
    """
    raw = getattr(player_scoring, "mPitState", None)
    if raw is None:
        log(
            "DEBUG",
            "player_scoring missing mPitState attribute",
            category="stint_tracker",
            action="get_pit_state",
        )
        return PitState.ON_TRACK

    try:
        # Allow numeric-like strings or integers; PitState is an IntEnum
        return PitState(int(raw))
    except (ValueError, TypeError) as exc:
        log(
            "WARNING",
            f"Invalid pit state value: {exc}",
            category="stint_tracker",
            action="get_pit_state",
        )
        return PitState.ON_TRACK

