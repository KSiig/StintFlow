"""
Overview view for stint tracking.

Displays stint tracking table and controls for managing race stints.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from ui.models import ModelContainer
from .StintTable import StintTable


class OverviewView(QWidget):
    """
    View for stint tracking overview.
    
    Shows stint data table with editing enabled.
    """
    
    def __init__(self, models: ModelContainer):
        """
        Initialize the overview window.
        
        Args:
            models: Container with selection_model and table_model
        """
        super().__init__()
        
        self.selection_model = models.selection_model
        self.table_model = models.table_model
        
        layout = QVBoxLayout(self)
        
        # Create stint table with editing enabled
        stint_table = StintTable(
            models=models,
            focus=True,          # Allow keyboard focus and selection
            auto_update=True,    # Refresh when session changes
            allow_editors=True   # Enable tire combo editors
        )
        
        layout.addWidget(stint_table)
