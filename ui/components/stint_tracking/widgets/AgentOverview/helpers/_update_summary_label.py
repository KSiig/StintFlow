from __future__ import annotations

from datetime import datetime, timedelta, timezone


def _update_summary_label(self, agents: list[dict]) -> None:
    """Update summary label as connected count over total discovered agents."""
    label = getattr(self, "_summary_label", None)
    if label is None:
        return

    total = len(agents)
    connected = 0

    for agent in agents:
        raw_heartbeat = agent.get('last_heartbeat')
        if not raw_heartbeat:
            continue

        try:
            heartbeat_dt = datetime.fromisoformat(str(raw_heartbeat))
        except Exception:
            continue

        if heartbeat_dt.tzinfo is None:
            heartbeat_dt = heartbeat_dt.replace(tzinfo=timezone.utc)

        try:
            heartbeat_dt = heartbeat_dt.astimezone()
        except Exception:
            pass

        heartbeat_age = datetime.now(heartbeat_dt.tzinfo) - heartbeat_dt
        if heartbeat_age <= timedelta(seconds=15):
            connected += 1

    label.setText(f"{connected} / {total} agent{'s' if total != 1 else ''}")
