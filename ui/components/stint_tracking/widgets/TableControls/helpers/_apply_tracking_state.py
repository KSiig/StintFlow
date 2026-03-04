"""Mirror tracking button appearance from config_options."""

from __future__ import annotations

from PyQt6.QtGui import QIcon

from ....config import ConfigLabels
from ui.utilities.load_icon import load_icon

ICON_PLAY = "resources/icons/race_config/play.svg"
ICON_STOP = "resources/icons/race_config/square.svg"
ICON_COLOR = "#1E1F24"


def _apply_tracking_state(self, is_running: bool) -> None:
    """Update tracking button appearance to reflect whether tracking is running."""
    label = ConfigLabels.BTN_STOP_TRACK if is_running else ConfigLabels.BTN_START_TRACK
    icon_path = ICON_STOP if is_running else ICON_PLAY
    pixmap = load_icon(icon_path, color=ICON_COLOR, size=16)
    self.tracking_btn.setText(label)
    self.tracking_btn.setIcon(QIcon(pixmap))
