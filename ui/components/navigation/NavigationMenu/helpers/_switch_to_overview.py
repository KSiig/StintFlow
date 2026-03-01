"""Switch to the Overview view and update active menu item."""

from ui.components.stint_tracking import OverviewView
from ...menu_item_factory import MenuItemConfig


def _switch_to_overview(self) -> None:
    """Switch to the Overview window and update active menu item."""
    if self.models and self.models.navigation_model:
        overview_widget = self.models.navigation_model.widgets.get(OverviewView)
        if overview_widget:
            self.models.navigation_model.set_active_widget(overview_widget)
            item_config: MenuItemConfig | None = self._menu_items.get(OverviewView)
            if item_config:
                self._set_active_menu_item(item_config)
