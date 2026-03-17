from __future__ import annotations

from PyQt6.QtWidgets import QLabel

from ui.components.common.ConfigButton import ConfigButton
from ui.utilities import FONT, get_fonts
from ....config import ConfigLabels


def _create_buttons(self) -> None:
    """Instantiate and wire all action buttons."""
    self.save_btn = ConfigButton(ConfigLabels.BTN_SAVE, icon_path="resources/icons/race_config/square-pen.svg", width="equal")
    self.cancel_btn = ConfigButton(ConfigLabels.BTN_CANCEL, width="equal")
    self.clone_btn = ConfigButton(ConfigLabels.BTN_CLONE, icon_path="resources/icons/race_config/copy.svg", width="equal")
    self.create_session_btn = ConfigButton(ConfigLabels.BTN_NEW_SESSION, width="fill")

    self.lbl_info = QLabel()
    self.lbl_info.setFont(get_fonts(FONT.header_input))
    self.lbl_info.setObjectName("InfoLabel")
    self.lbl_info.hide()

    self.save_btn.clicked.connect(self._save_config)
    self.cancel_btn.clicked.connect(self._cancel_changes)
    self.clone_btn.clicked.connect(self._clone_event)
    self.create_session_btn.clicked.connect(self._create_session)
