"""Switch to the Tracker view and update active menu item."""

from ui.components.stint_tracking import TrackerView
from ...menu_item_factory import MenuItemConfig


def _switch_to_tracker(self) -> None:
    """Switch to the Tracker window and update active menu item."""
    if self.models and self.models.navigation_model:
        tracker_widget = self.models.navigation_model.widgets.get(TrackerView)
        if tracker_widget:
            if not self._can_switch_menu_item(tracker_widget):
                return

            self.models.navigation_model.set_active_widget(tracker_widget)
            item_config: MenuItemConfig | None = self._menu_items.get(TrackerView)
            if item_config:
                self._set_active_menu_item(item_config)
