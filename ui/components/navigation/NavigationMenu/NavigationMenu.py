"""
Sidebar navigation menu for switching between application views.
"""

from PyQt6.QtWidgets import QWidget

from ui.models import ModelContainer
from ui.utilities.load_style import load_style

from .helpers import (
    _add_title_and_icon,
    _can_switch_menu_item,
    _create_layout,
    _create_menu_section,
    _set_active_menu_item,
    _switch_to_settings,
    _switch_to_strategies,
    _switch_to_tracker,
    _update_event_selection,
)


class NavigationMenu(QWidget):
    """Sidebar navigation menu for switching between application views."""

    _create_layout = _create_layout
    _update_event_selection = _update_event_selection
    _add_title_and_icon = _add_title_and_icon
    _can_switch_menu_item = _can_switch_menu_item
    _switch_to_tracker = _switch_to_tracker
    _switch_to_strategies = _switch_to_strategies
    _switch_to_settings = _switch_to_settings
    _set_active_menu_item = _set_active_menu_item
    _create_menu_section = _create_menu_section

    def __init__(self, parent: QWidget, models: ModelContainer = None) -> None:
        super().__init__(parent)
        self.models = models
        self._menu_items: dict[type, object] = {}
        self._active_menu_item = None

        load_style('resources/styles/navigation/navigation_menu.qss', widget=self)
        self._create_layout()

        if self.models and self.models.selection_model:
            self.models.selection_model.eventChanged.connect(self._update_event_selection)
            self.models.selection_model.sessionChanged.connect(self._update_event_selection)
