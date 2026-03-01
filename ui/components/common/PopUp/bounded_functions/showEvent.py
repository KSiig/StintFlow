"""Show event handler for PopUp dialogs."""

from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QTimer


def showEvent(self, event: QShowEvent) -> None:
    """Center on parent after showing."""
    QDialog.showEvent(self, event)
    QTimer.singleShot(0, self._center_on_parent)
