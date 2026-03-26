"""Helper to load team data and populate driver inputs.

This module defines ``_load_team``, which fetches the current team from the
database via :func:`core.database.get_team` and then calls ``_set_driver_names``
on the calling widget to populate the driver input fields.
"""

from __future__ import annotations

from core.database import get_team

def _load_team(self) -> None:
    """Load team from database and populate driver inputs."""
    team = get_team()
    if team:
        self._set_driver_names(team.get('drivers', []))
