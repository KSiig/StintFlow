"""Write the session-start header into the current log file."""

from datetime import datetime
from pathlib import Path

from .constants import HEADER_PREFIX


def write_session_header(path: Path, when: datetime | None = None) -> None:
    """Append a session-start header to *path*."""
    when = when or datetime.now()
    header = f"{HEADER_PREFIX} {when.strftime('%Y-%m-%d %H:%M:%S')} ==="
    with path.open("a", encoding="utf-8") as handle:
        handle.write(header + "\n")
