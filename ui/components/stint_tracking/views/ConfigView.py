"""
Configuration view for stint tracking.

Displays configuration options and stint tracker side-by-side.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout

from ui.models import ModelContainer
from core.errors import log_exception
from ..widgets import StintTable, ConfigOptions


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
        self.stint_table = None
        
        self._setup_ui(models)
    
    def _setup_ui(self, models: ModelContainer):
        """Build the UI layout with configuration options and stint table."""
        try:
            layout = QHBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(self.SPACING)
            
            # Add ConfigOptions component
            self.config_options = ConfigOptions(models)
            self.config_options.stint_created.connect(self.table_model.update_data)
            layout.addWidget(self.config_options)
            
            # Add stint table (read-only for config view)
            self.stint_table = StintTable(
                models=models,
                focus=False,         # No keyboard focus in config view
                auto_update=True,    # Refresh when session changes
                allow_editors=False  # Read-only display
            )
            layout.addWidget(self.stint_table)
            layout.addStretch()
        
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
