"""Read the auto-sync interval from user settings."""

from __future__ import annotations

from core.utilities import load_user_settings


def _get_auto_sync_interval_seconds(self) -> int:
    """Return the configured auto-sync interval in seconds with a safe fallback."""
    settings = load_user_settings()
    interval = settings.get("strategy_auto_sync_interval_seconds", 5) if isinstance(settings, dict) else 5

    try:
        interval = int(interval)
    except Exception:
        interval = 5

    return max(1, interval)