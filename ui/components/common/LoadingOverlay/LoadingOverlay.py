"""
Semi-transparent overlay displayed while the application performs
background initialization. Shows a busy indicator and a status label.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget

from .bounded_functions import set_status, show


class LoadingOverlay(QWidget):
    """Translucent overlay with a busy indicator and status label."""

    set_status = set_status
    show = show

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 128);")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setFixedWidth(128)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: white;")

        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)

        self.hide()
