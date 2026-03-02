"""Add the application title and icon to the navigation menu."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout

from ui.utilities import FONT, get_cached_icon, get_fonts
from ...constants import LOGO_SIZE, MENU_SPACING, TITLE_BOTTOM_MARGIN, ICON_LOGO, MENU_SECTION_ICON_COLOR


def _add_title_and_icon(self, layout: QVBoxLayout) -> None:
    """Add the application title and icon at the top of the menu."""
    title_layout = QHBoxLayout()
    title_layout.setSpacing(8)
    title_layout.setContentsMargins(MENU_SPACING, MENU_SPACING, 0, TITLE_BOTTOM_MARGIN)

    logo = QLabel()
    logo.setObjectName("TitleLogo")
    logo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    logo.setPixmap(get_cached_icon(ICON_LOGO, LOGO_SIZE, MENU_SECTION_ICON_COLOR))

    title = QLabel("StintFlow")
    title.setObjectName("TitleLabel")
    title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    title.setFont(get_fonts(FONT.title))

    title_layout.addWidget(logo)
    title_layout.addWidget(title)
    title_layout.addStretch()

    layout.addLayout(title_layout)
