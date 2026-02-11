"""
SectionHeader
----------------

Reusable section header widget used across the UI. Shows an optional
icon and a title in a horizontal layout. This implementation is robust
to missing icon/font resources and exposes small accessibility
improvements (tooltips / accessible names).
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from ui.utilities import get_fonts, FONT, load_icon


class SectionHeader(QWidget):
    """
    Common header widget for configuration or settings sections.

    Args:
        title: Display text for the header.
        icon_path: Path to an SVG/icon resource. If None, icon is omitted.
        icon_color: Hex color string to tint the icon (if supported).
        icon_size: Size (px) for the icon.
        spacing: Horizontal spacing between icon and title.
        parent: Optional parent widget.
    """

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

        # Optional icon — create only when a path is provided
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

        # Title label — attempt to apply the project's header font, but
        # degrade gracefully if the font system fails.
        title_label = QLabel(title)
        try:
            title_label.setFont(get_fonts(FONT.header_input))
        except Exception:
            # Missing font resource or other font error: continue without it
            pass

        title_label.setAccessibleName(f"{title} title")
        layout.addWidget(title_label)
        layout.addStretch()
