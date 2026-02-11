"""
StrategySettings component for the strategy tab placeholder.

Displays a placeholder for future strategy settings UI.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt

from core.utilities import resource_path
from core.errors import log
from ui.components.common import SectionHeader
from ui.models import ModelContainer

class StrategySettings(QWidget):
    """
    Placeholder widget for strategy settings/info box.
    """
    def __init__(self, parent=None, models: ModelContainer=None):
        super().__init__(parent)

        self.selection_model = models.selection_model
        self.table_model = models.table_model

        self._setup_styles()
        self._setup_ui()
    
    def _setup_styles(self) -> None:
        """Load and apply strategy settings stylesheet."""
        try:
            with open(resource_path('resources/styles/strategy_settings.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            log('WARNING', 'Strategy settings stylesheet not found', 
                category='strategy_settings', action='load_stylesheet')

    def _setup_ui(self):
        """Set up the UI layout for strategy settings."""

        layout = QVBoxLayout(self)
        frame = QFrame(self)
        frame.setObjectName("StrategySettingsFrame")
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)

        frame_layout = QVBoxLayout(frame)
        header = SectionHeader(
            title="Strategy Settings",
            icon_path="resources/icons/race_config/settings.svg",
            icon_color="#05fd7e",
            icon_size=20,
            spacing=8
        )
        header.setObjectName("StrategySettingsHeader")
        frame_layout.setContentsMargins(4, 8, 4, 8)

        frame_layout.addWidget(header)
        mean_stint_time = self.table_model._mean_stint_time if self.table_model else None
        mean_stint_time_label = self._create_mean_stint_time_label(mean_stint_time)
        frame_layout.addWidget(mean_stint_time_label)
        frame_layout.addStretch()

        frame.setLayout(frame_layout)

        layout.addWidget(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _create_mean_stint_time_label(self, mean_stint_time) -> QLabel:
        """Create a QLabel to display the mean stint time."""
        label = QLabel(f"Mean Stint Time: {mean_stint_time}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("MeanStintTimeLabel")
        return label
