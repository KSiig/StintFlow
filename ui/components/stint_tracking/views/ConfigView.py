"""
Configuration view for stint tracking.

Displays configuration options and stint tracker side-by-side.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy

from ui.models import ModelContainer
from core.errors import log_exception
from core.utilities import load_user_settings
from PyQt6.QtCore import QTimer
from ..widgets import StintTable, ConfigOptions, AgentOverview


class ConfigView(QWidget):
    """
    View for stint tracking configuration.
    
    Shows ConfigOptions (left) and StintTable (right) in a horizontal layout.
    """
    
    # Layout constants
    SPACING = 16
    
    def __init__(self, models: ModelContainer):
        """
        Initialize the config window.
        
        Args:
            models: Container with selection_model and table_model
        """
        super().__init__()
        
        self.selection_model = models.selection_model
        self.table_model = models.table_model
        self.config_options = None
        self.agent_overview = None
        self.stint_table = None
        self._poll_timer = None  # QTimer used during active tracking
        
        self._setup_ui(models)
    
    def _setup_ui(self, models: ModelContainer):
        """Build the UI layout with configuration options and stint table, wrapped in a QFrame."""
        from PyQt6.QtWidgets import QFrame
        try:
            frame = QFrame(self)
            frame.setObjectName("ConfigViewFrame")
            frame.setFrameShape(QFrame.Shape.NoFrame)
            frame.setFrameShadow(QFrame.Shadow.Plain)
            frame.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding
            )
            layout = QHBoxLayout(frame)
            layout.setContentsMargins(0, 0, 0, 16)
            layout.setSpacing(self.SPACING)

            # left column will stack the main options and the agent overview
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

            # load agents from database so the overview isn't empty
            self.agent_overview._load_agents()

            layout.addLayout(left_col)

            # Add stint table (read-only for config view)
            self.stint_table = StintTable(
                models=models,
                focus=False,         # No keyboard focus in config view
                auto_update=True,    # Refresh when session changes
                allow_editors=False  # Read-only display
            )
            layout.addWidget(self.stint_table)
            layout.addStretch()

            main_layout = QHBoxLayout(self)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.addWidget(frame)

        except Exception as e:
            log_exception(e, 'Failed to setup ConfigView UI',
                         category='config_view', action='setup_ui')
    
    def closeEvent(self, event):
        """Clean up signal connections on widget close."""
        try:
            if self.config_options:
                self.config_options.stint_created.disconnect(self.table_model.update_data)
        except Exception:
            pass  # Signal may already be disconnected
        
        super().closeEvent(event)

    # ------------------------------------------------------------------
    # agent polling helpers
    # ------------------------------------------------------------------
    def _on_tracker_started(self) -> None:
        """Begin reloading agent list: burst for a few seconds then normal pace."""
        # load once immediately; agent may register shortly thereafter
        self.agent_overview._load_agents()

        # start a short-lived 1‑second timer for the first 5 seconds
        self._startup_count = 0
        self._startup_timer = QTimer(self)
        self._startup_timer.timeout.connect(self._startup_tick)
        self._startup_timer.start(500)

    def _startup_tick(self) -> None:
        """Handler for the 1s startup timer; stops after 5 ticks."""
        self._startup_count += 1
        self.agent_overview._load_agents()
        if self._startup_count >= 5:
            if getattr(self, '_startup_timer', None):
                self._startup_timer.stop()
                self._startup_timer = None
            # once the burst is done, begin regular polling
            self._start_polling_timer()

    def _start_polling_timer(self) -> None:
        """Create and start the regular interval polling timer."""
        settings = load_user_settings()
        interval = settings.get('agent_poll_interval', 5)
        try:
            interval = int(interval)
        except Exception:
            interval = 5

        self._poll_timer = QTimer(self)
        self._poll_timer.timeout.connect(self.agent_overview._load_agents)
        self._poll_timer.start(interval * 1000)

    def _on_tracker_stopped(self) -> None:
        """Halt any active timers when the tracker shuts down."""
        if getattr(self, '_startup_timer', None):
            self._startup_timer.stop()
            self._startup_timer = None
        if getattr(self, '_poll_timer', None):
            self._poll_timer.stop()
            self._poll_timer = None
        self.agent_overview._load_agents()
