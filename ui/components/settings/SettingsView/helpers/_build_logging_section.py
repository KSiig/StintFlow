"""Build the logging settings section."""

from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QFormLayout, QFrame, QLabel, QLineEdit, QVBoxLayout

from ui.utilities import FONT, get_fonts


def _build_logging_section(self, parent_layout: QVBoxLayout) -> None:
    """Create the logging settings frame with retention field."""
    log_frame = QFrame()
    log_frame.setObjectName("LogFrame")
    log_layout = QVBoxLayout(log_frame)
    log_layout.setContentsMargins(0, 0, 0, 0)
    log_layout.setSpacing(12)

    title = QLabel("Logging")
    title.setFont(get_fonts(FONT.header_nav))
    log_layout.addWidget(title)

    form_layout = QFormLayout()
    form_layout.setContentsMargins(0, 0, 0, 0)
    form_layout.setSpacing(8)
    form_layout.setHorizontalSpacing(24)

    label = QLabel("Log retention (days)")
    label.setFont(get_fonts(FONT.input_lbl))
    retention_input = QLineEdit()
    retention_input.setFont(get_fonts(FONT.input_field))
    retention_input.setPlaceholderText("7")
    retention_input.setValidator(QIntValidator(0, 3650, self))
    form_layout.addRow(label, retention_input)
    self.inputs["retention_days"] = retention_input

    log_layout.addLayout(form_layout)
    parent_layout.addWidget(log_frame)
