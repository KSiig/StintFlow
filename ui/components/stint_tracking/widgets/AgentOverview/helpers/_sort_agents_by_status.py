from __future__ import annotations

from datetime import datetime, timedelta, timezone


def _sort_agents_by_status(agents: list[dict]) -> list[dict]:
    """Sort agents by status priority: Connected, Unavailable, then Offline."""

    def _status_rank(agent: dict) -> int:
        raw_heartbeat = agent.get('last_heartbeat')
        if not raw_heartbeat:
            return 2

        try:
            heartbeat_dt = datetime.fromisoformat(str(raw_heartbeat))
        except Exception:
            return 2

        if heartbeat_dt.tzinfo is None:
            heartbeat_dt = heartbeat_dt.replace(tzinfo=timezone.utc)

        try:
            heartbeat_dt = heartbeat_dt.astimezone()
        except Exception:
            pass

        heartbeat_age = datetime.now(heartbeat_dt.tzinfo) - heartbeat_dt

        if heartbeat_age <= timedelta(seconds=15):
            return 0
        if heartbeat_age <= timedelta(minutes=1):
            return 1
        return 2

    return sorted(agents, key=_status_rank)
