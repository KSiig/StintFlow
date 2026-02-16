"""
ConfigButton
--------------

QPushButton subclass used across configuration UI. Keeps the same
arguments as the old factory function but exposes them on a class so
callers can instantiate directly.
"""

from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtGui import QIcon
from ui.utilities import load_icon
from .constants import BTN_WIDTH_THIRD, BTN_WIDTH_HALF, BTN_WIDTH_FULL, BTN_HEIGHT

from core.utilities import resource_path
from core.errors import log

class ConfigButton(QPushButton):
    """Button with consistent sizing and optional icon.

    Args mirror the previous `create_config_button` factory for
    drop-in replacement.
    """

    def __init__(
        self,
        text: str = "",
        icon_path: str = None,
        icon_size: int = 16,
        icon_color: str = "#FFFFFF",
        width_type: str = "third",
        parent=None,
    ) -> None:
        super().__init__(text, parent)

        self._setup_styles()

        width_map = {
            "third": BTN_WIDTH_THIRD,
            "half": BTN_WIDTH_HALF,
            "full": BTN_WIDTH_FULL,
        }
        if width_type == "max":
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        elif width_type == "min":
            self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        else:
            button_width = width_map.get(width_type, BTN_WIDTH_THIRD)
            self.setFixedSize(button_width, BTN_HEIGHT)

        if icon_path:
            icon = load_icon(icon_path, size=icon_size, color=icon_color)
            if icon:
                self.setIcon(QIcon(icon))

    def _setup_styles(self) -> None:
        """Load and apply config button stylesheet."""
        try:
            with open(resource_path('resources/styles/config_button.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            log('WARNING', 'Config button stylesheet not found', 
                category='config_button', action='load_stylesheet')