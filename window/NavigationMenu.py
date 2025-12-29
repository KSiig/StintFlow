from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

class NavigationMenu(QWidget):
      def __init__(self, parent):
        super().__init__(parent)

        self.setContentsMargins(8, 8, 8, 8)
        self.setStyleSheet(
            """font-size: 16px;
               font-weight: 600;
            """
        )

        label = QLabel("Stint tracking")
        label.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout = QVBoxLayout(self)
        layout.addWidget(label)