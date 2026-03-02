"""Normalize various time representations to an HH:MM:SS string."""

from datetime import timedelta


def _normalize_time(value) -> str:
    """Return a normalized HH:MM:SS string from strings, timedeltas, or seconds."""
    if isinstance(value, timedelta):
        total = int(value.total_seconds())
        h = total // 3600
        m = (total % 3600) // 60
        s = total % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    if isinstance(value, (int, float)):
        total = int(value)
        h = total // 3600
        m = (total % 3600) // 60
        s = total % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    value_str = str(value)
    parts = [int(p) for p in value_str.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return f"{h:02d}:{m:02d}:{s:02d}"
