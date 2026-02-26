"""
Configuration view for stint tracking.

Displays configuration options and stint tracker side-by-side.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy

from ui.models import ModelContainer
from core.errors import log_exception
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
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(self.SPACING)

            # left column will stack the main options and an extras box
            left_col = QVBoxLayout()
            left_col.setContentsMargins(0, 0, 0, 0)
            left_col.setSpacing(12)

            self.config_options = ConfigOptions(models)
            self.config_options.stint_created.connect(self.table_model.update_data)
            left_col.addWidget(self.config_options)

            self.agent_overview = AgentOverview(models)
            left_col.addWidget(self.agent_overview)

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
