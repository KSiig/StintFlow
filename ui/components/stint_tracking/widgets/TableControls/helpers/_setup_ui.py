"""Build the TableControls layout."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy, QVBoxLayout

from ui.components.common import ConfigButton
from ui.components.stint_tracking.config.config_constants import ConfigLabels
from ui.components.stint_tracking.widgets.AgentOverview import AgentOverview


def _setup_ui(self) -> None:
    """Create the toggle button, tracking button, and connect signals."""
    # allow the entire control to expand vertically so its child frame
    # (which also expands) can fill the available height in the layout
    self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    outer = QVBoxLayout(self)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.setSpacing(0)

    self.frame = QFrame(self)
    self.frame.setObjectName("TableControlsFrame")
    outer.addWidget(self.frame)

    layout = QHBoxLayout(self.frame)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(16)

    btn_layout = QVBoxLayout()
    btn_layout.setSpacing(8)

    self.tracking_btn = ConfigButton(
        ConfigLabels.BTN_START_TRACK,
        icon_path="resources/icons/race_config/play.svg",
        icon_color="#1E1F24",
        width="content"
    )
    self.tracking_btn.setObjectName("TrackButton")
    self.tracking_btn.clicked.connect(self.config_options._toggle_track)
    btn_layout.addWidget(self.tracking_btn)

    self._left_column_toggle_btn = ConfigButton(ConfigLabels.BTN_HIDE_OPTIONS, width="fill")
    self._left_column_toggle_btn.clicked.connect(self._on_toggle_left_column)
    btn_layout.addWidget(self._left_column_toggle_btn)

    layout.addLayout(btn_layout)

    self.agent_overview = AgentOverview()
    self.agent_overview.selection_model = self.config_options.selection_model
    layout.addWidget(self.agent_overview)
    layout.setAlignment(self.agent_overview, Qt.AlignmentFlag.AlignHCenter)
    self.agent_overview._load_agents()

    if getattr(self.config_options.selection_model, 'sessionChanged', None):
        self.config_options.selection_model.sessionChanged.connect(self.agent_overview._load_agents)


    self.config_options.tracker_started.connect(lambda: self._apply_tracking_state(True))
    self.config_options.tracker_stopped.connect(lambda: self._apply_tracking_state(False))
    self._apply_tracking_state(self.config_options._tracking_active)
