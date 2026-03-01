"""Build the status display section."""

from PyQt6.QtWidgets import QLabel, QVBoxLayout

from ui.utilities import FONT, get_fonts


def _build_status_section(self, parent_layout: QVBoxLayout) -> None:
    """Create hint and status label widgets."""
    hint = QLabel("Connection string overrides host and credentials when set.")
    hint.setFont(get_fonts(FONT.header_input_hint))
    parent_layout.addWidget(hint)

    self.status_label = QLabel("")
    self.status_label.setFont(get_fonts(FONT.header_input_hint))
    parent_layout.addWidget(self.status_label)
