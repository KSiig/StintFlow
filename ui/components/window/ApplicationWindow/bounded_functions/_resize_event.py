from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QMainWindow

from ...constants import DRAGGABLE_AREA_HEIGHT, WORKSPACE_MARGINS_HOR


def resizeEvent(self, event: QEvent) -> None:
    """Handle window resize events and reposition overlays."""
    QMainWindow.resizeEvent(self, event)

    self.draggable_area.setGeometry(0, 0, self.width(), DRAGGABLE_AREA_HEIGHT)

    buttons_width = self.window_buttons.sizeHint().width()
    buttons_height = self.window_buttons.sizeHint().height()
    x_pos = self.width() - buttons_width - WORKSPACE_MARGINS_HOR
    y_pos = (DRAGGABLE_AREA_HEIGHT - buttons_height) // 2
    self.window_buttons.setGeometry(x_pos, y_pos, buttons_width, buttons_height)

    self.draggable_area.raise_()
    self.window_buttons.raise_()
