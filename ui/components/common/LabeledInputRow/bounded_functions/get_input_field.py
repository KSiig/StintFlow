"""Accessor for the internal input field."""

from PyQt6.QtWidgets import QLineEdit


def get_input_field(self) -> QLineEdit:
    """Return the internal QLineEdit for backwards compatibility."""
    return self.input_field
