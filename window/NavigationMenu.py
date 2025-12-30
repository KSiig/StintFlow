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
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
import os
import sys
from helpers import resource_path
from .Fonts import FONT, get_fonts

class NavigationMenu(QWidget):
      def __init__(self, parent):
        super().__init__(parent)

        self.setContentsMargins(8, 8, 8, 8)

        font = get_fonts(FONT.small_text)

        label = QLabel("Stint tracking")
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(font)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
