"""
LabeledInputRow

Reusable frame containing a label and single-line input field.
Designed to replace the old `create_config_row` helper with a
reusable component placed in the common components folder.
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLineEdit, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
from core.utilities import resource_path
from ui.utilities import get_fonts, FONT
from core.errors import log


class LabeledInputRow(QFrame):
    """
    Frame containing a label and a `QLineEdit` input.

    Args:
        title: Label text to show above the input.
        input_height: Optional fixed height for the input field (px).
        spacing: Optional spacing for the internal layout.
        parent: Optional parent widget.
    """

    def __init__(self, title: str, input_height: int = None, spacing: int = None, parent=None):
        super().__init__(parent)

        self._setup_styles()

        self.setObjectName("Setting")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        self.setContentsMargins(0, 0, 0, 0)

        main_box = QVBoxLayout(self)
        main_box.setContentsMargins(0, 0, 0, 0)
        if spacing is not None:
            main_box.setSpacing(spacing)

        # Label
        title_label = QLabel(title)
        title_label.setObjectName("SettingTitle")
        try:
            title_label.setFont(get_fonts(FONT.header_input))
        except Exception:
            pass

        # Input
        self.input_field = QLineEdit()
        self.input_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        if input_height is not None:
            self.input_field.setFixedHeight(input_height)
        try:
            self.input_field.setFont(get_fonts(FONT.input_field))
        except Exception:
            pass
        self.input_field.setReadOnly(True)
        self.input_field.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.input_field.setContentsMargins(0, 0, 0, 0)

        main_box.addWidget(title_label)
        main_box.addWidget(self.input_field, stretch=1)

    def _setup_styles(self) -> None:
        """Load and apply strategy settings stylesheet."""
        try:
            with open(resource_path('resources/styles/labeled_input_row.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            log('WARNING', 'Labeled input row stylesheet not found', 
                category='labeled_input_row', action='load_stylesheet')

    def get_input_field(self) -> QLineEdit:
        """Return the internal QLineEdit for backwards compatibility."""
        return self.input_field