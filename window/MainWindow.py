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
from .NavigationMenu import NavigationMenu
from .stint_tracking import SessionPicker, SelectionModel, TrackingMainWindow, StintTracker
from .NavigationModel import NavigationModel

import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 100, 1400, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.selection_model = SelectionModel()
        self.navigation_model = NavigationModel()

        main_window = TrackingMainWindow(self.selection_model)
        self.navigation_model.set_active_widget(main_window)

        central_widget = QWidget()
        self.title_bar = TitleBar(self)

        self.work_space_layout = QHBoxLayout()
        self.work_space_layout.setContentsMargins(11, 11, 11, 11)
        self.central_work_space_layout = QHBoxLayout()

        nav_menu = NavigationMenu(self, self.selection_model, self.navigation_model)

        self.work_space_layout.addWidget(nav_menu, alignment=Qt.AlignmentFlag.AlignLeft)
        self.work_space_layout.addLayout(self.central_work_space_layout)
        self.active_widget = self.navigation_model.active_widget
        self.central_work_space_layout.addWidget(self.active_widget)
        self.navigation_model.activeWidgetChanged.connect(self.change_workspace_widget)

        centra_widget_layout = QVBoxLayout()
        centra_widget_layout.setContentsMargins(0, 0, 0, 0)
        centra_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        centra_widget_layout.addWidget(self.title_bar)
        centra_widget_layout.addLayout(self.work_space_layout)

        central_widget.setLayout(centra_widget_layout)
        self.setCentralWidget(central_widget)

    def change_workspace_widget(self):
        # self.work_space_layout.replaceWidget(self.work_space_layout.)
        self.clear_layout(self.central_work_space_layout)
        new_widget = self.navigation_model.active_widget
        self.central_work_space_layout.addWidget(new_widget)
        self.active_widget = new_widget

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

            # Handle nested layouts
            sub_layout = item.layout()
            if sub_layout is not None:
                self.clear_layout(sub_layout)


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