from PyQt6.QtWidgets import QWidget


def setFixedHeight(self, height: int) -> None:
    """Set a fixed height for the button."""
    QWidget.setFixedHeight(self, height)
    self.dropdown.btn.setFixedHeight(height)