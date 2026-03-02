"""Inspect an existing log to determine its session start time."""

from datetime import datetime
from pathlib import Path

from .constants import HEADER_PATTERN


def parse_session_start(path: Path) -> datetime | None:
    """Return the session start time recorded in the first line of *path*.

    Returns ``None`` if the file is missing or does not contain the header.
    """
    try:
        with path.open("r", encoding="utf-8") as handle:
            first = handle.readline().rstrip("\n")
    except FileNotFoundError:
        return None

    match = HEADER_PATTERN.match(first)
    if not match:
        return None

    try:
        return datetime.strptime(match.group("ts"), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
