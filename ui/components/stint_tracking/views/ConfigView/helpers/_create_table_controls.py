"""Build the controls that sit above the stint table."""

from __future__ import annotations

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy

from ui.components.common import ConfigButton
from ui.components.stint_tracking.config.config_constants import ConfigLabels


def _create_table_controls(self):
    """Create the bar that holds the left toggle and tracking buttons."""
    controls_frame = QFrame(self)
    controls_frame.setObjectName("ConfigViewTableControls")

    layout = QHBoxLayout(controls_frame)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)

    self._left_column_toggle_btn = ConfigButton(ConfigLabels.BTN_HIDE_OPTIONS, width_type="half")
    self._left_column_toggle_btn.clicked.connect(self._toggle_left_column)
    layout.addWidget(self._left_column_toggle_btn)

    layout.addStretch()

    self.table_controls_tracking_btn = ConfigButton(
        ConfigLabels.BTN_START_TRACK,
        icon_path="resources/icons/race_config/play.svg",
        icon_color="#1E1F24",
    )
    self.table_controls_tracking_btn.clicked.connect(self.config_options._toggle_track)
    layout.addWidget(self.table_controls_tracking_btn)

    controls_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _apply_tracking_state(is_running: bool) -> None:
        source_btn = self.config_options.stop_btn if is_running else self.config_options.start_btn
        self.table_controls_tracking_btn.setText(source_btn.text())
        self.table_controls_tracking_btn.setIcon(source_btn.icon())

    self.config_options.tracker_started.connect(lambda: _apply_tracking_state(True))
    self.config_options.tracker_stopped.connect(lambda: _apply_tracking_state(False))
    _apply_tracking_state(self.config_options._tracking_active)

    self.table_controls_widget = controls_frame
    return controls_frame
