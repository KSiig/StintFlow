"""Normalize time strings that use 24:00:00."""


def normalize_24h_time(time_str: str) -> str:
    """Convert "24:xx:xx" into a valid "00:xx:xx" string."""
    if time_str.startswith("24:"):
        return "00:" + time_str[3:]
    return time_str
