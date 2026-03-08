"""Parse a time string into total seconds."""


def _parse_duration_seconds(duration_text: str) -> int:
    """Return the number of seconds represented by a HH:MM:SS string."""
    parts = str(duration_text).strip().split(':')
    if len(parts) != 3:
        return 0

    try:
        hours, minutes, seconds = (int(part) for part in parts)
    except ValueError:
        return 0

    return max((hours * 3600) + (minutes * 60) + seconds, 0)