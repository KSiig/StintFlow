"""
Section header widget with optional icon and title.
"""

from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget
from ui.utilities.fonts import FONT, get_fonts
from ui.utilities.load_icon import load_icon


class SectionHeader(QWidget):
    """Common header widget for configuration or settings sections."""

    DEFAULT_SPACING = 8
    DEFAULT_ICON_COLOR = "#000000"
    DEFAULT_ICON_SIZE = 16

    def __init__(
        self,
        title: str,
        icon_path: str = None,
        icon_color: str = DEFAULT_ICON_COLOR,
        icon_size: int = DEFAULT_ICON_SIZE,
        spacing: int = DEFAULT_SPACING,
        parent: QWidget = None,
    ) -> None:
        super().__init__(parent)
        self.title = title

        layout = QHBoxLayout(self)
        layout.setSpacing(spacing)
        layout.setContentsMargins(0, 0, 0, 0)

        if icon_path:
            icon_label = QLabel()
            try:
                icon = load_icon(icon_path, size=icon_size, color=icon_color)
            except Exception:
                icon = None

            if icon:
                icon_label.setPixmap(icon)

            icon_label.setFixedSize(icon_size, icon_size)
            icon_label.setAccessibleName(f"{title} icon")
            icon_label.setToolTip(title)
            layout.addWidget(icon_label)

        title_label = QLabel(title)
        try:
            title_label.setFont(get_fonts(FONT.header_input))
        except Exception:
            pass

        title_label.setAccessibleName(f"{title} title")
        layout.addWidget(title_label)
        layout.addStretch()
