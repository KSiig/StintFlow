"""Add a labeled input row to a form layout."""

from PyQt6.QtWidgets import QFormLayout, QLabel, QLineEdit

from ui.utilities import FONT, get_fonts


def _add_input(
    self,
    layout: QFormLayout,
    label_text: str,
    key: str,
    placeholder: str,
    is_password: bool = False,
) -> None:
    """Add a labeled line edit to the form layout."""
    label = QLabel(label_text)
    label.setFont(get_fonts(FONT.input_lbl))

    input_field = QLineEdit()
    input_field.setFont(get_fonts(FONT.input_field))
    input_field.setPlaceholderText(placeholder)
    if is_password:
        input_field.setEchoMode(QLineEdit.EchoMode.Password)

    layout.addRow(label, input_field)
    self.inputs[key] = input_field
