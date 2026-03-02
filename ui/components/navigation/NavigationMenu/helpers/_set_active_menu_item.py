"""Manage active state for navigation menu items."""

from ...menu_item_factory import update_menu_item_state


def _set_active_menu_item(self, item_config=None) -> None:
    """Set the active menu item and update visual states."""
    if item_config and item_config not in self._menu_items.values():
        return

    if self._active_menu_item:
        update_menu_item_state(self._active_menu_item, False)

    if item_config:
        update_menu_item_state(item_config, True)
        self._active_menu_item = item_config
