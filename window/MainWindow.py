from PyQt6.QtWidgets import ( 
        QMainWindow, 
        QTableView, 
        QPushButton, 
        QSizePolicy,
        QWidget, 
        QVBoxLayout, 
        QFrame,
        QHBoxLayout, 
        QPlainTextEdit, 
        QScrollArea,
        QComboBox, 
        QLineEdit, 
        QLabel
    )
from PyQt6.QtCore import QProcess, QTimer, Qt, QSize, Qt, QEvent
from PyQt6.QtGui import QFont
from .TitleBar import TitleBar
from .NavigationMenu import NavigationMenu
from .stint_tracking import SessionPicker, OverviewMainWindow, StintTracker, ConfigMainWindow
from .models import NavigationModel, SelectionModel

import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 100, 1400, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.selection_model = SelectionModel()
        self.navigation_model = NavigationModel()

        # main_window = ConfigMainWindow({"selection_model": self.selection_model})
        main_window = OverviewMainWindow({"selection_model": self.selection_model})
        self.navigation_model.set_active_widget(main_window)

        central_widget = QWidget()
        self.title_bar = TitleBar(self)

        self.work_space_layout = QHBoxLayout()
        self.work_space_layout.setContentsMargins(11, 11, 11, 11)
        self.central_work_space_layout = QHBoxLayout()

        nav_menu = NavigationMenu(self, self.selection_model, self.navigation_model)

        self.central_scroll_area = QScrollArea()
        self.central_scroll_area.setWidgetResizable(True)
        self.central_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.central_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.central_scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.central_container = QWidget()
        self.central_container.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding
        )
        self.central_container_layout = QHBoxLayout(self.central_container)
        self.central_container_layout.setContentsMargins(0, 0, 0, 0)

        self.central_scroll_area.setWidget(self.central_container)

        self.work_space_layout.addWidget(nav_menu, alignment=Qt.AlignmentFlag.AlignLeft)
        # self.work_space_layout.addLayout(self.central_work_space_layout)
        self.work_space_layout.addWidget(self.central_scroll_area)
        self.active_widget = self.navigation_model.active_widget
        # self.central_work_space_layout.addWidget(self.active_widget)
        self.central_container_layout.addWidget(self.active_widget)
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
        self.clear_layout(self.central_container_layout)
        new_widget = self.navigation_model.active_widget
        self.central_container_layout.addWidget(new_widget)
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