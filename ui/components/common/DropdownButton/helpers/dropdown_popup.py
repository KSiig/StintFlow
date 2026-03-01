"""Popup widget used by DropdownButton."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFontMetrics, QIcon
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QWidget


class DropdownPopup(QWidget):
    """Popup widget for dropdown selection."""

    valueChanged = pyqtSignal(str)

    def __init__(self, items: list[dict], popup_object_name: str, item_object_name: str, parent=None):
        super().__init__(parent, Qt.WindowType.Popup)
        self.setObjectName(f"{popup_object_name}Container")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowType.NoDropShadowWindowHint, True)

        popup_layout = QVBoxLayout(self)
        popup_layout.setContentsMargins(0, 0, 0, 0)
        popup_layout.setSpacing(0)

        frame = QFrame(self)
        frame.setObjectName(popup_object_name)
        popup_layout.addWidget(frame)

        layout = QVBoxLayout(frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.buttons = []
        max_text_width = 0

        for entry in items:
            display = entry.get('display', '')
            value = entry.get('value', display)
            icon = entry.get('icon')

            text_to_show = display if display else "(None)"
            parent_widget = self.parent()
            if parent_widget and hasattr(parent_widget, '_pad_text'):
                try:
                    text_to_show = parent_widget._pad_text(text_to_show)
                except Exception:
                    pass

            btn = QPushButton(text_to_show)
            btn.setObjectName(item_object_name)
            btn.setStyleSheet("text-align: left;")
            if icon:
                if isinstance(icon, str):
                    btn.setIcon(QIcon(icon))
                else:
                    btn.setIcon(icon)
            btn.clicked.connect(lambda checked, val=value: self._select_value(val))
            layout.addWidget(btn)
            self.buttons.append(btn)

            metrics = QFontMetrics(btn.font())
            text_width = metrics.boundingRect(btn.text()).width()
            if text_width > max_text_width:
                max_text_width = text_width

        self.setFixedWidth(max_text_width + 40)

    def _select_value(self, value: str) -> None:
        self.valueChanged.emit(value)
        self.hide()
