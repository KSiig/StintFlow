from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QMainWindow


def changeEvent(self, event: QEvent) -> None:
    """Handle window state changes to update window buttons."""
    if event.type() == QEvent.Type.WindowStateChange:
        self.window_buttons.window_state_changed(self.windowState())

    QMainWindow.changeEvent(self, event)
    event.accept()
