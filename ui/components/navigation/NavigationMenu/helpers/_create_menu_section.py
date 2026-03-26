"""Create a menu section layout with optional icon."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout

from ui.utilities import FONT, get_cached_icon, get_fonts
from ...constants import LOGO_SIZE, MENU_SECTION_ICON_COLOR, MENU_SPACING


def _create_menu_section(self, label: str, icon_path: str = None) -> QVBoxLayout:
    """Create a menu section with a header label and optional icon."""
    layout = QVBoxLayout()

    if icon_path:
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(MENU_SPACING, 0, 0, 4)
        header_layout.setSpacing(8)

        icon_label = QLabel()
        icon_label.setObjectName("NavMenuSectionIcon")
        icon_pixmap = get_cached_icon(icon_path, LOGO_SIZE, MENU_SECTION_ICON_COLOR)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(icon_label)

        text_label = QLabel(label)
        text_label.setObjectName("NavMenuSectionLabel")
        text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        text_label.setFont(self.font_menu_item)
        header_layout.addWidget(text_label)
        header_layout.addStretch()

        layout.setSpacing(4)
        layout.addLayout(header_layout)
    else:
        section_label = QLabel(label)
        section_label.setObjectName("NavMenuSectionLabel")
        section_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        section_label.setFont(self.font_menu_item)
        section_label.setContentsMargins(MENU_SPACING, 0, 0, 8)
        layout.setSpacing(8)
        layout.addWidget(section_label)

    return layout
