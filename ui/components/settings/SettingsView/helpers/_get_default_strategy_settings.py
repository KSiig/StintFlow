"""Defaults for strategy-related settings."""


def _get_default_strategy_settings(self) -> dict:
    """Return defaults for strategy settings."""
    # auto-sync interval defaults to 10 seconds
    return {"auto_sync_interval_seconds": 10}
