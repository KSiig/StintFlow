from __future__ import annotations

from ui.components.common import PopUp
from ....config import fetch_team_from_lmu


def _fetch_drivers(self) -> None:
    """Fetch driver names from LMU and populate inputs."""
    team = fetch_team_from_lmu()
    if team:
        self._set_driver_names(team)
        self.changed.emit()
        return

    dialog = PopUp(
        title="No team data found",
        message="Unable to fetch drivers because no team data is available.",
        buttons=["Ok"],
        type="error",
        parent=self,
    )
    dialog.exec()
