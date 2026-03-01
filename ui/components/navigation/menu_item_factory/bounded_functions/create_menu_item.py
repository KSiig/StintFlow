"""Factory to create a navigation menu item with optional icon."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel

from ui.components.common import ClickableWidget
from ui.utilities import FONT, get_cached_icon, get_fonts
from ..MenuItemConfig import MenuItemConfig
from ...constants import MENU_ITEM_ICON_COLOR, MENU_ITEM_ICON_SIZE, MENU_SPACING


def create_menu_item(label: str, callback, icon_path: str = None, menu_spacing=MENU_SPACING * 2) -> MenuItemConfig:
    """Create a navigation menu item with optional icon."""
    container = ClickableWidget(callback)
    container.setObjectName("MenuItem")
    container.setProperty("active", False)

    icon_label_widget = None

    if icon_path:
        layout = QHBoxLayout()
        layout.setContentsMargins(menu_spacing, 8, 0, 8)
        layout.setSpacing(8)

        icon_label_widget = QLabel()
        icon_pixmap = get_cached_icon(icon_path, MENU_ITEM_ICON_SIZE, MENU_ITEM_ICON_COLOR)
        icon_label_widget.setPixmap(icon_pixmap)
        icon_label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label_widget)

        text_label = QLabel(label)
        text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        text_label.setFont(get_fonts(FONT.menu_section))
        layout.addWidget(text_label)
        layout.addStretch()

        container.setLayout(layout)
    else:
        item = QLabel(label)
        item.setFont(get_fonts(FONT.menu_section))
        layout = QHBoxLayout()
        layout.setContentsMargins(menu_spacing, 8, 0, 8)
        layout.addWidget(item)
        layout.addStretch()
        container.setLayout(layout)

    return MenuItemConfig(
        label=label,
        callback=callback,
        widget=container,
        icon_path=icon_path,
        icon_label=icon_label_widget,
    )
