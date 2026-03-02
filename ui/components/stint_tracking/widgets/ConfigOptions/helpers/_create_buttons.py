from __future__ import annotations

from PyQt6.QtWidgets import QCheckBox, QLabel

from ui.components.common import ConfigButton
from ui.utilities import FONT, get_fonts
from ....config import ConfigLabels


def _create_buttons(self) -> None:
    """Instantiate and wire all action buttons."""
    self.edit_btn = ConfigButton(ConfigLabels.BTN_EDIT, icon_path="resources/icons/race_config/square-pen.svg")
    self.save_btn = ConfigButton(ConfigLabels.BTN_SAVE, icon_path="resources/icons/race_config/square-pen.svg")
    self.clone_btn = ConfigButton(ConfigLabels.BTN_CLONE, icon_path="resources/icons/race_config/copy.svg")
    self.create_session_btn = ConfigButton(ConfigLabels.BTN_NEW_SESSION, width_type="full")
    self.start_btn = ConfigButton(ConfigLabels.BTN_START_TRACK, icon_path="resources/icons/race_config/play.svg", icon_color="#1E1F24")
    self.stop_btn = ConfigButton(ConfigLabels.BTN_STOP_TRACK, icon_path="resources/icons/race_config/play.svg", icon_color="#1E1F24")
    self.start_btn.setObjectName("TrackButton")
    self.stop_btn.setObjectName("TrackButton")

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
    self.stop_btn.clicked.connect(self._toggle_track)
    self.start_btn.clicked.connect(self._toggle_track)
