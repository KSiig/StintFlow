from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
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

        nav_box = QVBoxLayout(frame)
        nav_box.setSpacing(24)

        stint_tracking_layout = self.create_layout_box("Stint tracking")
        # stint_tracking_layout = create_layout_box("Stint tracking")
        stint_tracking_layout.addWidget(self.create_row('fa6s.chart-line', 'Overview', font_small_text, OverviewMainWindow))
        stint_tracking_layout.addWidget(self.create_row('fa6s.chart-bar', 'Config', font_small_text, ConfigMainWindow))
        stint_tracking_layout.addWidget(self.create_row('fa6s.chess-board', 'Strategies', font_small_text, StrategiesMainWindow))
        # stint_tracking_layout.addWidget(create_row('fa6s.chart-line', 'iasdfadfafadd adsfa ang', font_small_text))

        # test_tracking_layout = create_layout_box("Stint tracking")
        # test_tracking_layout.addWidget(create_row('fa6s.chart-bar', 'Tracking', font_small_text))
        # test_tracking_layout.addWidget(create_row('fa6s.chart-line', 'ing', font_small_text))
        # test_tracking_layout.addWidget(create_row('fa6s.chart-line', 'iasdfadfafadd adsfa ang', font_small_text))

        nav_box.addLayout(stint_tracking_layout)
        # nav_box.addLayout(test_tracking_layout)
        nav_box.addStretch()

    def create_row(self, icon, label, font, widget):
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

        container.clicked.connect(lambda: self.test(widget))

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

    def test(self, widget):
        window = widget(self.models)
        self.navigation_model.set_active_widget(window)