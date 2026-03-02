"""Add an icon to a combo box positioned inside the left edge."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from ui.utilities import get_cached_icon
from ...constants import ICON_COLOR, ICON_SIZE, ICON_X_POSITION, ICON_Y_POSITION


def _add_combo_icon(self, combo_box, icon_path: str) -> None:
    """Attach an icon label to the combo box."""
    icon_pixmap = get_cached_icon(icon_path, ICON_SIZE, ICON_COLOR)

    icon_label = QLabel(combo_box)
    icon_label.setPixmap(icon_pixmap)
    icon_label.setFixedSize(ICON_SIZE, ICON_SIZE)
    icon_label.move(ICON_X_POSITION, ICON_Y_POSITION)
    icon_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
