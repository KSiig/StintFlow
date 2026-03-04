"""Build the navigation menu layout and items."""

from PyQt6.QtWidgets import QFrame, QVBoxLayout

from ...menu_item_factory import create_menu_item
from ui.components.navigation.SessionPicker import SessionPicker
from ui.components.stint_tracking import TrackerView, StrategiesView
from ui.components.settings import SettingsView
from ...constants import MENU_SPACING, MENU_WIDTH, ICON_COG, ICON_LOGO, ICON_SETTINGS, ICON_TARGET, ICON_TIMER
from ._add_title_and_icon import _add_title_and_icon
from ._create_menu_section import _create_menu_section
from ._set_active_menu_item import _set_active_menu_item
from ._switch_to_settings import _switch_to_settings
from ._switch_to_strategies import _switch_to_strategies
from ._switch_to_tracker import _switch_to_tracker


def _create_layout(self) -> None:
    """Create and configure the navigation menu layout."""
    self.setFixedWidth(MENU_WIDTH)
    self.setObjectName("NavMenu")

    frame = QFrame()
    frame.setObjectName("NavMenu")

    root_layout = QVBoxLayout(self)
    root_layout.setContentsMargins(0, 0, 0, 0)
    root_layout.addWidget(frame)

    menu_layout = QVBoxLayout(frame)
    menu_layout.setSpacing(MENU_SPACING)
    menu_layout.setContentsMargins(0, 8, 0, 0)

    _add_title_and_icon(self, menu_layout)

    stint_tracking_layout = _create_menu_section(self, "Stint tracking", ICON_TIMER)

    # Use a single primary entry called "Tracker" that points to the combined
    # tracker landing view (serves as the app landing/track control screen).
    tracker_item = create_menu_item("Tracker", lambda: _switch_to_tracker(self), ICON_COG)
    tracker_item.window_class = TrackerView
    self._menu_items[TrackerView] = tracker_item
    stint_tracking_layout.addWidget(tracker_item.widget)

    strategies_item = create_menu_item("Strategies", lambda: _switch_to_strategies(self), ICON_TARGET)
    strategies_item.window_class = StrategiesView
    self._menu_items[StrategiesView] = strategies_item
    stint_tracking_layout.addWidget(strategies_item.widget)

    menu_layout.addLayout(stint_tracking_layout)

    _set_active_menu_item(self, tracker_item)

    menu_layout.addStretch()

    settings_item = create_menu_item("Settings", lambda: _switch_to_settings(self), ICON_SETTINGS, menu_spacing=32)
    settings_item.window_class = SettingsView
    settings_item.widget.setObjectName("MenuItemSettings")
    self._menu_items[SettingsView] = settings_item
    menu_layout.addWidget(settings_item.widget)

    self.session_picker = SessionPicker(models=self.models)
    menu_layout.addWidget(self.session_picker)
