"""Build the ConfigView layout."""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy

from ui.components.stint_tracking.widgets import AgentOverview, ConfigOptions, StintTable
from core.errors import log_exception


def _setup_ui(self, models) -> None:
    """Build the UI with configuration options and stint table."""
    try:
        frame = QFrame(self)
        frame.setObjectName("ConfigViewFrame")
        frame.setFrameShape(QFrame.Shape.NoFrame)
        frame.setFrameShadow(QFrame.Shadow.Plain)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 16)
        layout.setSpacing(self.SPACING)

        left_col = QVBoxLayout()
        left_col.setContentsMargins(0, 0, 0, 0)
        left_col.setSpacing(12)

        self.config_options = ConfigOptions(models)
        self.config_options.stint_created.connect(self.table_model.update_data)
        self.config_options.tracker_started.connect(self._on_tracker_started)
        self.config_options.tracker_stopped.connect(self._on_tracker_stopped)
        left_col.addWidget(self.config_options)

        self.agent_overview = AgentOverview()
        left_col.addWidget(self.agent_overview)
        self.agent_overview._load_agents()

        layout.addLayout(left_col)

        self.stint_table = StintTable(
            models=models,
            focus=False,
            auto_update=True,
            allow_editors=False,
        )
        layout.addWidget(self.stint_table)
        layout.addStretch()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(frame)
    except Exception as exc:
        log_exception(exc, "Failed to setup ConfigView UI", category="config_view", action="setup_ui")
