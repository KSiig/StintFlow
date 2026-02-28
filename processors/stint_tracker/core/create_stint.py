"""Create and upsert an official stint document.

This module builds a compact stint document from LMU game state and
inserts (or deduplicates) it in MongoDB using `upsert_official_stint`.
"""

from typing import Any, Dict

from bson import ObjectId

from core.database import upsert_official_stint
from core.errors import log, log_exception
from processors.stint_tracker.helpers import (
    _get_tire_state,
    _detect_tire_changes,
    TIRE_POSITIONS,
    _normalize_pit_time,
)


_LOG_CATEGORY = "stint_tracker"
_LOG_ACTION = "create_stint"


def create_stint(
    remaining_time: str,
    player_vehicle: Any,
    player_scoring: Any,
    num_penalties: int,
    session_id: str,
    driver_name: str,
    tires_coming_in: Dict[str, Any],
) -> str | None:
    """Create a stint record in the database or return None on skip/failure.

    The function prefers early returns for validation and keeps the happy
    path unindented for readability.
    """
    # Validate session_id early
    if not ObjectId.is_valid(session_id):
        log("ERROR", f"Invalid session_id format: {session_id}",
            category=_LOG_CATEGORY, action=_LOG_ACTION)
        return None

    try:
        # Penalty served -> skip recording
        if num_penalties > player_scoring.mNumPenalties:
            log("INFO", "Penalty served - skipping stint creation",
                category=_LOG_CATEGORY, action=_LOG_ACTION)
            return None

        # Outgoing tire snapshot
        tires_outgoing = _get_tire_state(player_vehicle)

        # Assemble tire payload
        tire_data: Dict[str, Any] = {
            pos: {"incoming": tires_coming_in.get(pos, {}), "outgoing": tires_outgoing[pos]}
            for pos in TIRE_POSITIONS
        }
        tire_data["tires_changed"] = _detect_tire_changes(tires_outgoing)

        # Normalize time for dedupe across trackers
        normalized_time = _normalize_pit_time(remaining_time) or remaining_time
        if normalized_time == remaining_time:
            # If _normalize_pit_time failed to change format, warn once
            log("WARNING", f"Pit end time used as-is: {remaining_time}",
                category=_LOG_CATEGORY, action=_LOG_ACTION)

        stint_key = f"{session_id}:{normalized_time}"

        stint = {
            "session_id": ObjectId(session_id),
            "driver": driver_name,
            "pit_end_time": remaining_time,
            "pit_end_time_bucket": normalized_time,
            "stint_key": stint_key,
            "official": True,
            "tire_data": tire_data,
        }

        stint_id, was_inserted = upsert_official_stint(stint, stint_key)
        if not stint_id:
            return None

        if was_inserted:
            log("INFO", f"Created stint {stint_id} for driver {driver_name}",
                category=_LOG_CATEGORY, action=_LOG_ACTION)
        else:
            log("INFO", f"Deduped stint {stint_id} for driver {driver_name}",
                category=_LOG_CATEGORY, action=_LOG_ACTION)

        return stint_id

    except Exception as exc:
        log_exception(exc, "Failed to create stint",
                      category=_LOG_CATEGORY, action=_LOG_ACTION)
        return None
