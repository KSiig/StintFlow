"""Delete archived log files older than the configured retention window."""

from datetime import datetime, timedelta
from pathlib import Path


def purge_old_logs(directory: Path, max_age_days: int = 30) -> None:
    """Delete archived log files older than *max_age_days* in *directory*."""
    if max_age_days == 30:
        from core.utilities.settings.load_user_settings import load_user_settings

        settings = load_user_settings()
        logging_settings = settings.get("logging", {}) if isinstance(settings, dict) else {}
        retention = logging_settings.get("retention_days")
        if isinstance(retention, int) and retention > 0:
            max_age_days = retention

    if max_age_days <= 0:
        return

    cutoff = datetime.now() - timedelta(days=max_age_days)
    for entry in directory.iterdir():
        if not entry.name.startswith("stintflow-"):
            continue
        try:
            mtime = datetime.fromtimestamp(entry.stat().st_mtime)
        except Exception:
            continue
        if mtime < cutoff:
            try:
                entry.unlink()
            except Exception:
                pass
