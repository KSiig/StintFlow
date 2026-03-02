"""Switch to the Strategies view and update active menu item."""

from ui.components.stint_tracking import StrategiesView
from ...menu_item_factory import MenuItemConfig


def _switch_to_strategies(self) -> None:
    """Switch to the Strategies window and update active menu item."""
    if self.models and self.models.navigation_model:
        strategies_widget = self.models.navigation_model.widgets.get(StrategiesView)
        if strategies_widget:
            self.models.navigation_model.set_active_widget(strategies_widget)
            item_config: MenuItemConfig | None = self._menu_items.get(StrategiesView)
            if item_config:
                self._set_active_menu_item(item_config)
