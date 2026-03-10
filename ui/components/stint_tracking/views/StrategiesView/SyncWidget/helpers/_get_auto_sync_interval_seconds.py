"""Read the auto-sync interval from user settings."""

from __future__ import annotations

from core.utilities import load_user_settings


def _get_auto_sync_interval_seconds(self) -> int:
    """Return the configured auto-sync interval in seconds with a safe fallback."""
    settings = load_user_settings()
    if isinstance(settings, dict):
        strat = settings.get("strategy", {})
        interval = strat.get("auto_sync_interval_seconds", 10) if isinstance(strat, dict) else 10
    else:
        interval = 10

    try:
        interval = int(interval)
    except Exception:
        interval = 10

    return max(1, interval)