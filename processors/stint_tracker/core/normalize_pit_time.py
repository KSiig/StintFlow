"""
Normalize pit end time to a bucket window.

Used for stint deduplication across multiple trackers.
"""


def normalize_pit_time(pit_end_time: str, window_seconds: int = 2) -> str | None:
    """
    Normalize a HH:MM:SS time string into a bucketed time string.

    Args:
        pit_end_time: Time string in HH:MM:SS format
        window_seconds: Bucket size in seconds

    Returns:
        Normalized HH:MM:SS string, or None if parsing fails
    """
    if window_seconds <= 0:
        return None

    parts = pit_end_time.split(':')
    if len(parts) != 3:
        return None

    try:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
    except ValueError:
        return None

    if hours < 0 or minutes < 0 or seconds < 0:
        return None

    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    bucket_seconds = (total_seconds // window_seconds) * window_seconds

    norm_hours = bucket_seconds // 3600
    remaining = bucket_seconds % 3600
    norm_minutes = remaining // 60
    norm_seconds = remaining % 60

    return f"{norm_hours:02d}:{norm_minutes:02d}:{norm_seconds:02d}"
