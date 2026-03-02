"""Update active state styling for a navigation menu item."""

from ui.utilities import get_cached_icon
from ...constants import MENU_ITEM_ICON_COLOR, MENU_ITEM_ICON_COLOR_ACTIVE, MENU_ITEM_ICON_SIZE
from ..helpers import _refresh_widget_style
from ..MenuItemConfig import MenuItemConfig


def update_menu_item_state(item_config: MenuItemConfig, is_active: bool) -> None:
    """Update menu item's active state including visual styling and icon color."""
    widget = item_config.widget

    widget.setProperty("active", is_active)
    _refresh_widget_style(widget)

    if item_config.icon_label and item_config.icon_path:
        icon_color = MENU_ITEM_ICON_COLOR_ACTIVE if is_active else MENU_ITEM_ICON_COLOR
        icon_pixmap = get_cached_icon(item_config.icon_path, MENU_ITEM_ICON_SIZE, icon_color)
        item_config.icon_label.setPixmap(icon_pixmap)

    item_config.is_active = is_active
