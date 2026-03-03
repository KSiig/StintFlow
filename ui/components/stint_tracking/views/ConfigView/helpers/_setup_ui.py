"""Build the ConfigView layout."""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy

from ui.components.stint_tracking.widgets import AgentOverview, ConfigOptions, StintTable, TableControls
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

        left_container = QFrame(frame)
        left_container.setFrameShape(QFrame.Shape.NoFrame)
        left_container.setLayout(left_col)
        left_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.left_column_container = left_container
        layout.addWidget(left_container)

        right_container = QFrame(frame)
        right_container.setFrameShape(QFrame.Shape.NoFrame)
        right_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        table_controls = TableControls(
            config_options=self.config_options,
            on_toggle_left_column=self._toggle_left_column,
        )
        self._left_column_toggle_btn = table_controls._left_column_toggle_btn
        right_layout.addWidget(table_controls)

        self.stint_table = StintTable(
            models=models,
            focus=False,
            auto_update=True,
            allow_editors=False,
        )
        right_layout.addWidget(self.stint_table)
        right_layout.setStretch(1, 1)

        layout.addWidget(right_container)
        layout.setStretchFactor(right_container, 1)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(frame)
    except Exception as exc:
        log_exception(exc, "Failed to setup ConfigView UI", category="config_view", action="setup_ui")
