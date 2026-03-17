from __future__ import annotations

from core.database import get_team

def _load_team(self) -> None:
    """Load team from database and populate driver inputs."""
    self._clear_drivers()
    team = get_team()
    if team:
        self._set_driver_names(team.get('drivers', []))
