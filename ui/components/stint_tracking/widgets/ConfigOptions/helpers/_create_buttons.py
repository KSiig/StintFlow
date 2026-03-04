from __future__ import annotations

from PyQt6.QtWidgets import QCheckBox, QLabel

from ui.components.common.ConfigButton import ConfigButton
from ui.utilities import FONT, get_fonts
from ....config import ConfigLabels


def _create_buttons(self) -> None:
    """Instantiate and wire all action buttons."""
    self.edit_btn = ConfigButton(ConfigLabels.BTN_EDIT, icon_path="resources/icons/race_config/square-pen.svg", width_type="half")
    self.save_btn = ConfigButton(ConfigLabels.BTN_SAVE, icon_path="resources/icons/race_config/square-pen.svg", width_type="half")
    self.clone_btn = ConfigButton(ConfigLabels.BTN_CLONE, icon_path="resources/icons/race_config/copy.svg", width_type="half")
    self.create_session_btn = ConfigButton(ConfigLabels.BTN_NEW_SESSION, width_type="full")

    self.practice_cb = QCheckBox(text="Practice")
    self.lbl_info = QLabel()
    self.practice_cb.setFont(get_fonts(FONT.input_field))
    self.lbl_info.setFont(get_fonts(FONT.header_input))
    self.lbl_info.setObjectName("InfoLabel")
    self.lbl_info.hide()

    self.edit_btn.clicked.connect(self._toggle_edit)
    self.save_btn.clicked.connect(lambda: (self._save_config(), self._toggle_edit()))
    self.clone_btn.clicked.connect(self._clone_event)
    self.create_session_btn.clicked.connect(self._create_session)
