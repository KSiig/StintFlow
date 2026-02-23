"""
Semi-transparent overlay displayed while the application performs
background initialization.  Shows a busy indicator and a status label.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar


class LoadingOverlay(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # translucent background so underlying layout isn't completely hidden
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 128);")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # busy indicator
        self.progress.setFixedWidth(128)

        self.status_label = QLabel('')
        self.status_label.setStyleSheet('color: white;')

        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)

        self.hide()

    def set_status(self, text: str) -> None:
        """Update the status text shown below the spinner."""
        self.status_label.setText(text)

    def show(self) -> None:
        super().show()
        self.raise_()
