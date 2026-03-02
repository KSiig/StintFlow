from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from ui.utilities import FONT, get_fonts
from ui.utilities.load_style import load_style

from .bounded_functions import showEvent
from .helpers import _center_on_parent, _handle_click, _set_icon


class PopUp(QDialog):
    """Frameless popup dialog with icon, title, message, and buttons."""

    showEvent = showEvent
    _set_icon = _set_icon
    _center_on_parent = _center_on_parent
    _handle_click = _handle_click

    def __init__(self, title: str, message: str, buttons=None, type: str = "info", parent: QWidget = None):
        super().__init__(parent)
        load_style('resources/styles/common/popup.qss', widget=self)

        self._icon_map = {
            "info": ("resources/icons/popup/info.svg", "#3b82f6"),
            "error": ("resources/icons/popup/circle-x.svg", "#ef4444"),
            "warning": ("resources/icons/popup/triangle-alert.svg", "#f59e0b"),
            "critical": ("resources/icons/popup/circle-alert.svg", "#dc2626"),
        }
        icon_path, self._icon_color = self._icon_map.get(type, ("resources/icons/popup/info.svg", "#3b82f6"))
        self.setFixedSize(510, 248)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.container = QFrame()
        self.container.setObjectName("ContentFrame")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(28, 28, 28, 28)

        self.container.setStyleSheet(
            f"""
            QFrame#ContentFrame {{
                background-color: white;
                border-radius: 8px;
                border-left: 2px solid {self._icon_color};
            }}
            """
        )

        icon_frame = QFrame()
        icon_frame.setObjectName("IconFrame")
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._set_icon(type)
        icon_layout.addWidget(self.icon_label)
        self.container_layout.addWidget(icon_frame)

        self.container_layout.addSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title_label.setFont(get_fonts(FONT.dialog_header))
        self.container_layout.addWidget(self.title_label)

        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label.setFont(get_fonts(FONT.dialog_msg))
        self.container_layout.addWidget(self.label)

        if buttons is None:
            buttons = ["Ok"]
        button_row = QWidget()
        button_row.setObjectName("ButtonRow")
        button_layout = QHBoxLayout(button_row)
        button_layout.setContentsMargins(0, 16, 0, 0)
        button_layout.setSpacing(16)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        for btn_text in buttons:
            _, color = self._icon_map.get(type, ("", "#3b82f6"))
            btn = QPushButton(btn_text)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {color};
                    border-radius: 4px;
                    padding: 6px 12px;
                    color: white;
                }}
                """
            )
            btn.clicked.connect(lambda _, b=btn_text: self._handle_click(b))
            button_layout.addWidget(btn)
        self.container_layout.addWidget(button_row)

        self.main_layout.addWidget(self.container)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(25)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(4)
        self.shadow.setColor(QColor(0, 0, 0, 180))
        self.container.setGraphicsEffect(self.shadow)

        self.setMinimumWidth(390)
