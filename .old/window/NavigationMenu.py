from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QStackedLayout,
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStyle,
    QFrame,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QPushButton,
)
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
import os
import sys
from helpers import resource_path
from .Fonts import FONT, get_fonts
from .ClickableWidget import ClickableWidget
from .stint_tracking import (
    StintTracker, 
    SessionPicker, 
    OverviewMainWindow, 
    ConfigMainWindow, 
    StrategiesMainWindow
)
import qtawesome as qta
from .models import NavigationModel, SelectionModel


class NavigationMenu(QWidget):
    def __init__(self, parent, models = {"selection_model": SelectionModel()}):
        super().__init__(parent)

        self.models = models
        self.selection_model = models['selection_model']
        self.navigation_model = models['navigation_model']
        self.table_model = models['table_model']
        self.windows = {}  # store instantiated windows

        with open(resource_path('styles/navigation_menu.qss'), 'r') as f:
            style = f.read()

        self.setStyleSheet(style)
        # self.setContentsMargins(8, 8, 8, 8)
        self.setFixedWidth(200)

        font_small_text = get_fonts(FONT.text_small)

        frame = QFrame()
        frame.setObjectName("NavMenu")

        root_widget_layout = QVBoxLayout(self)   
        root_widget_layout.addWidget(frame)

        self.nav_box = QVBoxLayout(frame)
        self.nav_box.setSpacing(24)
        self.session_picker = SessionPicker(models)

        stint_tracking_layout = self.create_layout_box("Stint tracking")
        stint_tracking_layout.addWidget(self.create_row('fa6s.chart-line', 'Overview', font_small_text, OverviewMainWindow))
        stint_tracking_layout.addWidget(self.create_row('fa6s.chart-bar', 'Config', font_small_text, ConfigMainWindow))
        stint_tracking_layout.addWidget(self.create_row('fa6s.chess-board', 'Strategies', font_small_text, StrategiesMainWindow))

        self.nav_box.addLayout(stint_tracking_layout)
        self.nav_box.addStretch()

        self.nav_box.addWidget(self.session_picker)
        self.selection_model.eventChanged.connect(self.update_event_selection)
        self.selection_model.sessionChanged.connect(self.update_event_selection)

    def update_event_selection(self):
        self.session_picker.reload()


    # Helper: add a nav row AND create the window in the stack
    def add_nav_row(self, layout, icon, text, font, window_cls):
        # Create clickable row
        row_widget = self.create_row(icon, text, font, window_cls)
        layout.addWidget(row_widget)

        # Instantiate window if not already done
        if window_cls not in self.windows:
            window = window_cls(self.models)
            window.setParent(self.stack_container)
            self.stack_layout.addWidget(window)
            self.windows[window_cls] = window

        # Connect nav click to show the window
        row_widget.clicked.connect(lambda cls=window_cls: self.show_window(cls))

    def create_row(self, icon, label, font, widget_cls):
        container = ClickableWidget()
        fa6s_icon = qta.icon(icon, color='#000')
        icon_label = QLabel()
        icon_label.setMaximumSize(24, 24)
        icon_label.setPixmap(fa6s_icon.pixmap(QSize(24, 24)))

        text_label = QLabel(label)
        text_label.setFont(font)

        row_layout = QHBoxLayout(container)
        row_layout.addWidget(icon_label)
        row_layout.addWidget(text_label)
        row_layout.setSpacing(16)
        row_layout.setContentsMargins(8,0,0,0)

        container.clicked.connect(lambda widget_cls=widget_cls: self.set_active_widget(widget_cls))

        widget = widget_cls(self.models)
        self.navigation_model.add_widget(widget_cls, widget)

        return container

    def create_layout_box(self, label):
        font = get_fonts(FONT.header_nav)
        label = QLabel(label)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(font)
        label.setContentsMargins(0,0,0,8)

        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.addWidget(label)

        return layout

    def set_active_widget(self, widget_cls):
        self.navigation_model.set_active_widget(widget_cls)
