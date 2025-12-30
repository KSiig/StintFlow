from PyQt6.QtWidgets import ( 
        QMainWindow, 
        QTableView, 
        QPushButton, 
        QWidget, 
        QVBoxLayout, 
        QHBoxLayout, 
        QPlainTextEdit, 
        QComboBox, 
        QLineEdit, 
        QLabel
    )
from PyQt6.QtCore import QProcess, QTimer, Qt, QSize, Qt, QEvent
from PyQt6.QtGui import QFont
from .TitleBar import TitleBar
from .StintTracker import StintTracker
from .NavigationMenu import NavigationMenu
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 100, 1400, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        central_widget = QWidget()
        self.title_bar = TitleBar(self)

        work_space_layout = QHBoxLayout()
        work_space_layout.setContentsMargins(11, 11, 11, 11)
        main_window = StintTracker()
        nav_menu = NavigationMenu(self)
        work_space_layout.addWidget(nav_menu)
        work_space_layout.addWidget(main_window)

        centra_widget_layout = QVBoxLayout()
        centra_widget_layout.setContentsMargins(0, 0, 0, 0)
        centra_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        centra_widget_layout.addWidget(self.title_bar)
        centra_widget_layout.addLayout(work_space_layout)

        central_widget.setLayout(centra_widget_layout)
        self.setCentralWidget(central_widget)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)