"""
Overview view for stint tracking.

Displays stint tracking table and controls for managing race stints.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from ui.models import ModelContainer


class OverviewView(QWidget):
    """
    View for stint tracking overview.
    
    Shows stint data table and tracking controls.
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
        
        # TODO: Add StintTracker component with allow_editors=True
        # For now, show placeholder text
        placeholder = QLabel("Stint Tracker Overview - Coming Soon")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("font-size: 24px; color: #666;")
        
        layout.addWidget(placeholder)
