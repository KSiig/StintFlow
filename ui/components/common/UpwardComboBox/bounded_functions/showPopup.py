"""Override to show popup above the combo box."""

from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QComboBox


def showPopup(self) -> None:
    """Show the popup above the combo box instead of below."""
    QComboBox.showPopup(self)
    popup = self.view().parentWidget()
    if popup:
        combo_pos = self.mapToGlobal(QPoint(0, 0))
        popup_height = popup.height()
        popup.move(combo_pos.x(), combo_pos.y() - popup_height)
