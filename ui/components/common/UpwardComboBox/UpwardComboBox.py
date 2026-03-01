"""
ComboBox that opens its dropdown above instead of below.
"""

from PyQt6.QtWidgets import QComboBox

from .bounded_functions import showPopup


class UpwardComboBox(QComboBox):
    """ComboBox that opens its dropdown above instead of below."""

    showPopup = showPopup
