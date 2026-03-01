"""Show the overlay and raise it above siblings."""

from PyQt6.QtWidgets import QWidget


def show(self) -> None:
    """Show the overlay and ensure it is on top."""
    QWidget.show(self)
    self.raise_()
