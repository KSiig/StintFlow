"""
StrategySettings component for the strategy tab placeholder.

Displays a placeholder for future strategy settings UI.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt

from core.utilities import resource_path
from core.errors import log
from ui.components.common import LabeledInputRow, SectionHeader, ConfigButton
from ..config import ConfigLabels
from ui.components.stint_tracking.config.config_constants import ConfigLayout
from ui.models import ModelContainer
from datetime import timedelta

class StrategySettings(QWidget):
    """
    Placeholder widget for strategy settings/info box.
    """
    def __init__(self, parent=None, models: ModelContainer=None):
        super().__init__(parent)

        self.selection_model = models.selection_model
        self.table_model = models.table_model
        self.inputs = {}

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
        frame_layout.setSpacing(12)

        frame_layout.addWidget(header)
        mean_stint_time = self.table_model._mean_stint_time if self.table_model else None

        # Buttons (Edit / Save)
        btn_row = QVBoxLayout()
        self.edit_btn = ConfigButton(ConfigLabels.BTN_EDIT, icon_path="resources/icons/race_config/square-pen.svg", width_type="half")
        self.save_btn = ConfigButton(ConfigLabels.BTN_SAVE, icon_path="resources/icons/race_config/square-pen.svg", width_type="half")
        self.save_btn.hide()
        self.edit_btn.clicked.connect(self._toggle_edit)
        self.save_btn.clicked.connect(self._on_save_clicked)


        self._create_labeled_input_rows(frame_layout)
        self._set_inputs(mean_stint_time=mean_stint_time)

        frame_layout.addStretch()

        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.save_btn)
        frame_layout.addLayout(btn_row)

        frame.setLayout(frame_layout)

        layout.addWidget(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _create_labeled_input_rows(self, layout: QVBoxLayout):
        """Create labeled input rows for strategy settings."""
                # Create and store input field references
        for field_id, title in [
            ("mean_stint_time", "Mean Stint Time"),
        ]:
            card = LabeledInputRow(title=title, input_height=ConfigLayout.INPUT_HEIGHT)
            self.inputs[field_id] = card.get_input_field()
            layout.addWidget(card)

    def _toggle_edit(self):
        """Toggle edit mode for the input rows."""
        # If save button visible, switch to view mode
        if self.save_btn.isVisible():
            self.save_btn.hide()
            self.edit_btn.show()
            for widget in self.inputs.values():
                try:
                    widget.setReadOnly(True)
                    widget.setProperty('editable', False)
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)
                except Exception:
                    pass
        else:
            # Enter edit mode
            self.edit_btn.hide()
            self.save_btn.show()
            for widget in self.inputs.values():
                try:
                    widget.setReadOnly(False)
                    widget.setProperty('editable', True)
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)
                except Exception:
                    pass

    def _on_save_clicked(self):
        """Placeholder save handler — does not persist changes yet."""
        log('INFO', 'StrategySettings save clicked (placeholder)',
            category='strategy_settings', action='save_clicked')
        # Revert to view mode after pressing save
        self._toggle_edit()

    def _set_inputs(self, mean_stint_time=None):
        """Set the values of the input fields."""
        if mean_stint_time is not None:
            mean_stint_time_str = self._format_mean_stint_time(mean_stint_time)

            # Ensure the input field exists before setting text
            widget = self.inputs.get("mean_stint_time")
            if widget is not None:
                widget.setText(mean_stint_time_str)

    def _format_mean_stint_time(self, mean_stint_time) -> str:
        """Return a H:MM:SS string for the provided mean_stint_time.

        Accepts datetime.timedelta, string (possibly containing microseconds),
        or numeric seconds. Falls back to str(value) on unexpected input.
        """
        # Handle timedelta objects by stripping microseconds
        if isinstance(mean_stint_time, timedelta):
            return str(mean_stint_time).split('.', 1)[0]

        # Handle string representations like '0:27:07.800000'
        if isinstance(mean_stint_time, str):
            return mean_stint_time.split('.', 1)[0]

        # Try to interpret as seconds (numeric) and format H:MM:SS
        try:
            total_seconds = int(float(mean_stint_time))
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        except Exception:
            return str(mean_stint_time)