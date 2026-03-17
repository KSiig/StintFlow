"""
Reusable frame containing a label and single-line input field.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QFrame, QLineEdit, QSizePolicy, QVBoxLayout

from ui.utilities import FONT, get_fonts
from ui.utilities.load_style import load_style

from .bounded_functions import get_input_field


class LabeledInputRow(QFrame):
    """Frame containing a label and a `QLineEdit` input."""

    get_input_field = get_input_field

    def __init__(self, title: str, input_height: int = None, spacing: int = None, parent=None, on_text_change=None):
        super().__init__(parent)

        load_style('resources/styles/common/labeled_input_row.qss', widget=self)

        self.setObjectName("Setting")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        self.setContentsMargins(0, 0, 0, 0)

        main_box = QVBoxLayout(self)
        main_box.setContentsMargins(0, 0, 0, 0)
        if spacing is not None:
            main_box.setSpacing(spacing)

        title_label = QLabel(title)
        title_label.setObjectName("SettingTitle")
        try:
            title_label.setFont(get_fonts(FONT.header_input))
        except Exception:
            pass

        self.input_field = QLineEdit()
        self.input_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        if input_height is not None:
            self.input_field.setFixedHeight(input_height)
        try:
            self.input_field.setFont(get_fonts(FONT.input_field))
        except Exception:
            pass
        self.input_field.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.input_field.setContentsMargins(0, 0, 0, 0)
        if on_text_change is not None:
            self.input_field.textEdited.connect(on_text_change)

        main_box.addWidget(title_label)
        main_box.addWidget(self.input_field, stretch=1)
