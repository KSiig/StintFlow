"""
Configuration view for stint tracking.

Displays configuration options and stint tracker side-by-side.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

from ui.models import ModelContainer
from .StintTable import StintTable


class ConfigView(QWidget):
    """
    View for stint tracking configuration.
    
    Shows ConfigOptions (left) and StintTable (right) in a horizontal layout.
    """
    
    def __init__(self, models: ModelContainer):
        """
        Initialize the config window.
        
        Args:
            models: Container with selection_model and table_model
        """
        super().__init__()
        
        self.selection_model = models.selection_model
        self.table_model = models.table_model
        
        main_layout = QVBoxLayout(self)
        h_layout = QHBoxLayout()
        
        # TODO: Add ConfigOptions component
        # config_options = ConfigOptions(models)
        # config_options.stint_created.connect(self.table_model.update_data)
        # h_layout.addWidget(config_options)
        config_placeholder = QLabel("Config Options - Coming Soon")
        config_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        config_placeholder.setStyleSheet("font-size: 18px; color: #666;")
        h_layout.addWidget(config_placeholder)
        
        # Add stint table (read-only for config view)
        stint_table = StintTable(
            models=models,
            focus=False,         # No keyboard focus in config view
            auto_update=True,    # Refresh when session changes
            allow_editors=False  # Read-only display
        )
        h_layout.addWidget(stint_table)
        
        main_layout.addLayout(h_layout)
