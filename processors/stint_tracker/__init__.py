"""Stint tracker package public surface.

This package contains the independent processor responsible for
monitoring LMU shared memory and creating stint records when pit
stops are detected. The package intentionally exposes only the
core functions used by external callers.

Note: run.py is a script-style entrypoint and is not re-exported here.
"""

from .core import create_stint, track_session

__all__ = (
    "create_stint",
    "track_session",
)
