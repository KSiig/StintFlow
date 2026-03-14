"""Main tracking loop for the stint tracker.

Poll the LMU shared memory, detect pit activity for the player and
create stint records when pit stops are completed.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List

from core.errors import log
from processors.stint_tracker.helpers import (
    _get_tire_state,
    _get_practice_baseline_time,
    _get_pit_state,
    PitState,
    _is_in_garage,
    _calculate_remaining_time,
    _maybe_update_heartbeat,
    _maybe_cleanup_stale_agents,
    _get_player_info,
    _get_game_session,
    GAME_SESSION,
    _maybe_refresh_game_session,
    _store_tires_remaining_at_green_flag,
)
from .create_stint import create_stint


# --- Configuration ---
POLLING_FREQUENCY: int = 1  # Hz
GAME_SESSION_TTL_SECONDS: float = 5.0

_LOG_CATEGORY = "stint_tracker"
_LOG_ACTION = "track_session"
_TIRE_SNAPSHOT_GAME_SESSIONS = {
    GAME_SESSION.BEFORE,
    GAME_SESSION.FORMATION,
    GAME_SESSION.RACE,
}


def track_session(
    lmu_telemetry: Any,
    lmu_scoring: Any,
    session_id: str,
    drivers: List[str],
    agent_name: str | None = None,
    dry_run: bool = False,
) -> None:
    """Track session and create stints when pit stops are detected.

    The function is intended to run in a standalone process. It performs
    a simple event loop that updates a heartbeat, cleans stale agents
    periodically, and inspects LMU memory for player pit activity.
    """

    # Runtime state
    pit_stop_in_progress: bool = False
    num_penalties: int = 0
    garage_time_snapshot: str = "00:00:00"
    tracking_enabled: bool = False
    tracked_driver_name: str = ""
    tires_coming_in: Dict[str, Any] = {}
    practice_baseline_time: str | None = None
    current_game_session: GAME_SESSION = _get_game_session()
    last_game_session_refresh_at: float = time.monotonic()
    previous_pit_state: PitState | None = None
    tire_snapshot_sessions_recorded: set[GAME_SESSION] = set()
    previous_game_session: GAME_SESSION = GAME_SESSION.UNKNOWN

    if current_game_session == GAME_SESSION.PRACTICE:
        practice_baseline_time = _get_practice_baseline_time(session_id)
        log("DEBUG", f"Practice mode baseline time: {practice_baseline_time}",
            category=_LOG_CATEGORY, action=_LOG_ACTION)

    if current_game_session != GAME_SESSION.UNKNOWN:
        log("INFO", f"Detected initial game session: {current_game_session.name}",
            category=_LOG_CATEGORY, action=_LOG_ACTION)

    if current_game_session in _TIRE_SNAPSHOT_GAME_SESSIONS and not dry_run:
        _store_tires_remaining_at_green_flag(session_id)
        tire_snapshot_sessions_recorded.add(current_game_session)

    log("INFO", f"Tracking session {session_id} ({'dry run' if dry_run else 'live'})",
        category=_LOG_CATEGORY, action=_LOG_ACTION)

    last_cleanup = time.time()

    # Main loop
    while True:
        # --- housekeeping -------------------------------------------------
        _maybe_update_heartbeat(agent_name)
        last_cleanup = _maybe_cleanup_stale_agents(last_cleanup)

        # Dry-run keeps heartbeats/cleanup but skips LMU access
        if dry_run:
            print("next loop")
            time.sleep(1.0 / POLLING_FREQUENCY)
            continue

        # --- player/session info -----------------------------------------
        player_info = _get_player_info(lmu_telemetry, lmu_scoring, drivers)
        if not player_info:
            log("DEBUG", "No player info found in LMU memory; retrying",
                category=_LOG_CATEGORY, action=_LOG_ACTION)
            time.sleep(1.0 / POLLING_FREQUENCY)
            continue

        player_vehicle, player_scoring, driver_name = player_info
        pit_state = _get_pit_state(player_scoring)
        # refresh cached session according to TTL or pit-state changes
        current_game_session, last_game_session_refresh_at = _maybe_refresh_game_session(
            current_game_session,
            last_game_session_refresh_at,
            previous_pit_state,
            pit_state,
            GAME_SESSION_TTL_SECONDS,
        )

        if current_game_session == GAME_SESSION.QUALIFYING:
            log("DEBUG", "Qualifying session detected; stint tracking disabled",
                category=_LOG_CATEGORY, action=_LOG_ACTION)
            time.sleep(1.0 / POLLING_FREQUENCY)
            continue

        # Detect transition to PRACTICE session
        if previous_game_session != GAME_SESSION.PRACTICE and current_game_session == GAME_SESSION.PRACTICE:
            practice_baseline_time = _get_practice_baseline_time(session_id)
            log("INFO", f"Transitioned to PRACTICE session. Reloaded baseline time: {practice_baseline_time}",
                category=_LOG_CATEGORY, action=_LOG_ACTION)

        # Update previous_game_session for next loop
        previous_game_session = current_game_session

        if (
            current_game_session in _TIRE_SNAPSHOT_GAME_SESSIONS
            and current_game_session not in tire_snapshot_sessions_recorded
        ):
            _store_tires_remaining_at_green_flag(session_id)
            tire_snapshot_sessions_recorded.add(current_game_session)

        # Capture tire state when coming into pits
        if pit_state == PitState.COMING_IN and not pit_stop_in_progress:
            log("DEBUG", f"Driver {driver_name} entering pits",
                category=_LOG_CATEGORY, action=_LOG_ACTION)
            tires_coming_in = _get_tire_state(player_vehicle)
            tracked_driver_name = driver_name

        # Practice mode: enable tracking once player is in garage
        if current_game_session == GAME_SESSION.PRACTICE and not tracking_enabled:
            if _is_in_garage(player_scoring):
                log("INFO", "Player in garage - tracking enabled",
                    category=_LOG_CATEGORY, action=_LOG_ACTION)
                tracking_enabled = True
            else:
                log("INFO", "Return to garage - tracking disabled",
                    category=_LOG_CATEGORY, action=_LOG_ACTION)
                time.sleep(1.0)
                continue

        # When in garage we snapshot remaining time for later calculations
        if _is_in_garage(player_scoring):
            print("__info__:stint_tracker:player_in_garage")
            pit_stop_in_progress = True
            garage_time_snapshot = _calculate_remaining_time(lmu_scoring)

        # Detect pit stop completion and create stint
        if not pit_stop_in_progress and pit_state == PitState.LEAVING:
            log("INFO", f"Driver {tracked_driver_name} leaving pits - creating stint",
                category=_LOG_CATEGORY, action=_LOG_ACTION)
            pit_stop_in_progress = True

            # Compute remaining time depending on mode
            if current_game_session == GAME_SESSION.PRACTICE and practice_baseline_time:
                remaining_time = _calculate_remaining_time(
                    lmu_scoring,
                    start_time=garage_time_snapshot,
                    offset_time=practice_baseline_time,
                )
                log("DEBUG", f"Practice stint time: {remaining_time} (baseline: {practice_baseline_time}, offset: {garage_time_snapshot})",
                    category=_LOG_CATEGORY, action=_LOG_ACTION)
            else:
                remaining_time = _calculate_remaining_time(lmu_scoring)

            # Create database record for the stint
            stint_id = create_stint(
                remaining_time=remaining_time,
                player_vehicle=player_vehicle,
                player_scoring=player_scoring,
                num_penalties=num_penalties,
                session_id=session_id,
                driver_name=tracked_driver_name,
                tires_coming_in=tires_coming_in,
            )

            if current_game_session == GAME_SESSION.PRACTICE and stint_id:
                practice_baseline_time = remaining_time
                log("DEBUG", f"Updated practice baseline to: {practice_baseline_time}",
                    category=_LOG_CATEGORY, action=_LOG_ACTION)

        # Reset state when back on track
        if pit_state == PitState.ON_TRACK and pit_stop_in_progress:
            log("DEBUG", f"Driver {tracked_driver_name} back on track",
                category=_LOG_CATEGORY, action=_LOG_ACTION)
            num_penalties = player_scoring.mNumPenalties
            pit_stop_in_progress = False

        previous_pit_state = pit_state

        time.sleep(1.0 / POLLING_FREQUENCY)
