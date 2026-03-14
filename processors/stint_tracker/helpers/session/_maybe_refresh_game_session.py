"""Utility for TTL-based game-session caching.

This helper encapsulates the refresh policy used by the tracker loop.
It avoids inlining the "is it time to call the REST API" logic in the
main loop and centralises the logging of session changes.
"""

import time

from core.errors import log
from .GAME_SESSION import GAME_SESSION
from ._get_game_session import _get_game_session
from ..pit_functions import PitState


def _maybe_refresh_game_session(
    current: GAME_SESSION,
    last_refresh_at: float,
    prev_pit_state: PitState | None,
    cur_pit_state: PitState,
    ttl_seconds: float = 5.0,
) -> tuple[GAME_SESSION, float]:
    """Return an updated session and refresh timestamp.

    The session is refreshed if either the cached value is older than
    ``ttl_seconds`` or the pit state has changed (``prev_pit_state`` is not
    ``None`` and differs from ``cur_pit_state``). The actual HTTP
    request is performed by ``_get_game_session``; if that returns
    ``GAME_SESSION.UNKNOWN`` the original ``current`` value is preserved.

    If a new valid session is obtained and differs from ``current`` the change
    is logged at INFO level. ``last_refresh_at`` is always updated when a
    refresh attempt is performed, regardless of its outcome, so callers can
    rely on it for TTL calculations.
    """
    now = time.monotonic()
    needs_refresh = (now - last_refresh_at) >= ttl_seconds
    state_changed = prev_pit_state is not None and cur_pit_state != prev_pit_state

    if not (needs_refresh or state_changed):
        # nothing to do
        return current, last_refresh_at

    refreshed = _get_game_session()
    new_refresh_at = time.monotonic()

    if refreshed != GAME_SESSION.UNKNOWN:
        if refreshed != current:
            log(
                "INFO",
                f"Game session changed from {current.name} to {refreshed.name}",
                category="stint_tracker",
                action="track_session",
            )
        current = refreshed

    return current, new_refresh_at
