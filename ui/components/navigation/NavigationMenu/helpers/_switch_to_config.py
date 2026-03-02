"""Switch to the Config view and update active menu item."""

from ui.components.stint_tracking import ConfigView
from ...menu_item_factory import MenuItemConfig


def _switch_to_config(self) -> None:
    """Switch to the Config window and update active menu item."""
    if self.models and self.models.navigation_model:
        config_widget = self.models.navigation_model.widgets.get(ConfigView)
        if config_widget:
            self.models.navigation_model.set_active_widget(config_widget)
            item_config: MenuItemConfig | None = self._menu_items.get(ConfigView)
            if item_config:
                self._set_active_menu_item(item_config)
