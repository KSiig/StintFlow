from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QToolButton


def _create_button(self, icon_path: str, callback) -> QToolButton:
    """Create a styled window control button."""
    button = QToolButton(self)
    icon = QIcon(icon_path)
    button.setIcon(icon)
    button.setIconSize(QSize(self.BUTTON_ICON_SIZE, self.BUTTON_ICON_SIZE))
    button.clicked.connect(callback)
    button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    button.setFixedSize(QSize(self.BUTTON_SIZE, self.BUTTON_SIZE))
    return button
