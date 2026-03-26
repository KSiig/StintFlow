"""
ConfigButton
--------------

QPushButton subclass used across configuration UI. Keeps the same
arguments as the old factory function but exposes them on a class so
callers can instantiate directly.
"""

from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtGui import QIcon

from ui.utilities import FONT, get_fonts
from ui.utilities.load_icon import load_icon
from ui.utilities.load_style import load_style

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
        width: int | str = "content",
        parent=None,
        font = FONT.text_body,
        padding_height = 4,
        padding_width = 0,
    ) -> None:
        super().__init__(text, parent)
        load_style('resources/styles/common/config_button.qss', widget=self)

        font_obj = get_fonts(font)
        self.setFont(font_obj)
        self.setContentsMargins(padding_width, padding_height, padding_width, padding_height)

        # Allow explicit pixel width by passing an int for `width`.
        if isinstance(width, int):
            self.setFixedWidth(width)
        elif width == "fill":
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.setMinimumWidth(0)
        elif width == "equal":
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.setMinimumWidth(0)
            self.setProperty("equal_width", True)
        else:
            # default: wrap around content
            self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

        if icon_path:
            icon = load_icon(icon_path, size=icon_size, color=icon_color)
            if icon:
                self.setIcon(QIcon(icon))
