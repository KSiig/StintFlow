"""Switch to the Settings view and update active menu item."""

from ...menu_item_factory import MenuItemConfig
from ui.components.settings import SettingsView


def _switch_to_settings(self) -> None:
    """Switch to the Settings window and update active menu item."""
    if self.models and self.models.navigation_model:
        settings_widget = self.models.navigation_model.widgets.get(SettingsView)
        if settings_widget:
            self.models.navigation_model.set_active_widget(settings_widget)
            item_config: MenuItemConfig | None = self._menu_items.get(SettingsView)
            if item_config:
                self._set_active_menu_item(item_config)
