"""Session-aware rotation of the primary log file."""

import sys
from datetime import datetime
from pathlib import Path

from ._state import process_start
from .parse_session_start import parse_session_start
from .purge_old_logs import purge_old_logs


def rotate_old_log(path: Path) -> None:
    """Ensure a fresh log file is available at *path* before logging starts."""
    if not path.exists():
        return

    try:
        size = path.stat().st_size
    except Exception:
        return

    if size == 0:
        return

    session = parse_session_start(path)
    if session is not None:
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
        except Exception:
            mtime = None
        if mtime is not None and mtime >= process_start:
            return

    try:
        timestamp = datetime.fromtimestamp(path.stat().st_mtime)
    except Exception:
        timestamp = datetime.now()

    base = timestamp.strftime("%Y%m%d-%H%M%S")
    dest = path.with_name(f"stintflow-{base}.log")
    counter = 1
    while dest.exists():
        dest = path.with_name(f"stintflow-{base}_{counter}.log")
        counter += 1

    try:
        path.rename(dest)
    except Exception as exc:
        print(f"Warning: could not rotate log file: {exc}", file=sys.stderr)

    purge_old_logs(path.parent)
