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
    QPushButton,
)
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
import os
import sys
from helpers import resource_path
from .Fonts import FONT, get_fonts
from .ClickableWidget import ClickableWidget
import qtawesome as qta

class NavigationMenu(QWidget):
      def __init__(self, parent):
        super().__init__(parent)

        # self.setContentsMargins(8, 8, 8, 8)
        self.setFixedWidth(200)

        font_small_text = get_fonts(FONT.small_text)

        nav_box = QVBoxLayout(self)
        nav_box.setSpacing(24)

        stint_tracking_layout = create_layout_box("Stint tracking")
        # stint_tracking_layout = create_layout_box("Stint tracking")
        stint_tracking_layout.addWidget(create_row('fa6s.chart-bar', 'Tracking', font_small_text))
        # stint_tracking_layout.addWidget(create_row('fa6s.chart-line', 'ing', font_small_text))
        # stint_tracking_layout.addWidget(create_row('fa6s.chart-line', 'iasdfadfafadd adsfa ang', font_small_text))

        # test_tracking_layout = create_layout_box("Stint tracking")
        # test_tracking_layout.addWidget(create_row('fa6s.chart-bar', 'Tracking', font_small_text))
        # test_tracking_layout.addWidget(create_row('fa6s.chart-line', 'ing', font_small_text))
        # test_tracking_layout.addWidget(create_row('fa6s.chart-line', 'iasdfadfafadd adsfa ang', font_small_text))

        nav_box.addLayout(stint_tracking_layout)
        # nav_box.addLayout(test_tracking_layout)
        nav_box.addStretch()

def create_row(icon, label, font):
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

    container.clicked.connect(test)

    return container

def create_layout_box(label):
    font = get_fonts(FONT.nav_header)
    label = QLabel(label)
    label.setAlignment(Qt.AlignmentFlag.AlignTop)
    label.setFont(font)
    label.setContentsMargins(0,0,0,8)

    layout = QVBoxLayout()
    layout.setSpacing(8)
    layout.addWidget(label)

    return layout

def test():
    print(('it clicked'))