"""
Helpers for rotating the StintFlow log file on application startup.

A simple session‑based rotation mechanism is used:

* When the first caller in a given application run configures the
  logger, the existing ``stintflow.log`` (if any) is examined.
* If the file does **not** begin with the special session‑start header,
  it is renamed to ``stintflow-<timestamp>.log`` where ``<timestamp>``
  is taken from the header (if present) or the file's modification time.
  Counters are appended if the target name is already in use.
* A header line is written to the new ``stintflow.log`` so subsequent
  processes in the same run can detect that rotation has already
  happened and avoid renaming again.

Keeping the logic in its own module follows the project's "one function
per file" guideline and keeps ``log_error`` focused on logger
configuration.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ``load_user_settings`` is imported lazily inside the function to avoid a
# circular import problem.  If we import it at module level the package
# may still be initialising and ``load_user_settings`` can resolve to the
# submodule itself (see traceback in bug report).

# header line written to each new log file.  parse_session_start uses a
# regular expression built from these constants so the format must stay in
# sync.
HEADER_PREFIX = "=== StintFlow session started:"
HEADER_FORMAT = HEADER_PREFIX + " %Y-%m-%d %H:%M:%S ==="
_HEADER_RE = re.compile(rf"^{re.escape(HEADER_PREFIX)} (?P<ts>\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}) ===$")


def parse_session_start(path: Path) -> datetime | None:
    """Return the session start time recorded in the first line of *path*.

    Args:
        path: path to inspect; may not exist.

    Returns:
        ``datetime`` object if the first line matches the header pattern,
        otherwise ``None``.  Any IO errors are propagated to the caller.
    """
    try:
        with path.open("r", encoding="utf-8") as f:
            first = f.readline().rstrip("\n")
    except FileNotFoundError:
        return None

    m = _HEADER_RE.match(first)
    if not m:
        return None

    try:
        return datetime.strptime(m.group("ts"), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # malformed timestamp; treat as if no header present
        return None


# record the time this interpreter was started; used to distinguish
# a header written by a previous run from the one created during the
# current session.  using ``datetime.now()`` is sufficient because the
# logger is configured very early.
_process_start = datetime.now()


def rotate_old_log(path: Path) -> None:
    """Ensure a fresh log file is available at *path*.

    The existing file is renamed unless it already contains a session
    header that was written during the current process run.  Headers from
    earlier runs (even though they look identical) are ignored and the
    file is archived normally.  The archive name is
    ``stintflow-YYYYMMDD-HHMMSS.log`` (with ``_1`` etc added to avoid
    collisions).  Any error during renaming is written to stderr but does
    **not** raise; the application should continue even if rotation fails.
    """
    if not path.exists():
        # nothing to do
        return

    try:
        size = path.stat().st_size
    except Exception:
        # unable to stat, give up
        return

    if size == 0:
        # empty log file; no need to archive it
        return

    session = parse_session_start(path)
    if session is not None:
        # a header is present; check the file's modification time to
        # decide whether it belongs to this run.  ``_process_start`` is set
        # once on module import.
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
        except Exception:
            mtime = None
        if mtime is not None and mtime >= _process_start:
            # header written during this run; nothing to rotate.
            return
        # otherwise fall through and rotate the file as if no header

    # choose a timestamp for the archive name.  prefer mtime so we
    # approximate when the old session began; fall back to now if stat
    # fails.
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
    except Exception as e:
        # logger is not configured yet; print to stderr so it is still
        # visible during startup failures.  Do not raise.
        print(f"Warning: could not rotate log file: {e}", file=sys.stderr)

    # after rotation we can optionally clean up old archives; this keeps the
    # log directory from growing indefinitely.  the default retention period
    # is 30 days (or the value configured by the user via settings) but
    # callers may invoke ``purge_old_logs`` directly with an explicit
    # value if they wish.
    purge_old_logs(path.parent)


# small helper used by log_error to write the header; exposed for testing
# only.
def purge_old_logs(directory: Path, max_age_days: int = 30) -> None:
    """Delete archived log files older than *max_age_days* in *directory*.

    The default retention period is 30 days; however if the user has
    configured a value via the SettingsView (``logging.retention_days``)
    that number will be used instead when the caller does not explicitly
    pass a different ``max_age_days`` value.

    Args:
        directory: path containing log files (typically the parent of
            ``stintflow.log``).
        max_age_days: number of days to retain; files with a modification
            time older than this threshold are removed.  A non-positive
            value disables purging.  If left at the default and a
            configuration value is present it will be overridden.

    This helper does **not** remove the current ``stintflow.log`` file.  It
    only considers files whose names start with ``stintflow-`` (i.e. the
    archived sessions).
    """
    # honour user-configured retention if provided and caller didn't
    # supply a custom value.  import locally to avoid circular imports
    # when this module is pulled in via ``core.errors.__init__``.
    if max_age_days == 30:
        from core.utilities.settings.load_user_settings import load_user_settings

        settings = load_user_settings()
        logging_settings = settings.get('logging', {}) if isinstance(settings, dict) else {}
        retention = logging_settings.get('retention_days')
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
            # unable to stat, skip it rather than raising
            continue
        if mtime < cutoff:
            try:
                entry.unlink()
            except Exception:
                # best-effort purge; ignore errors
                pass


def write_session_header(path: Path, when: datetime | None = None) -> None:
    """Append a session-start header to *path*.

    If *when* is omitted the current time is used.  The file is created if
    it does not already exist.
    """
    when = when or datetime.now()
    header = f"{HEADER_PREFIX} {when.strftime('%Y-%m-%d %H:%M:%S')} ==="
    # open in append mode to avoid truncation; the caller has already
    # rotated the existing file if necessary.
    with path.open("a", encoding="utf-8") as f:
        f.write(header + "\n")
