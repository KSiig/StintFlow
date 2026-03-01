"""
Sidebar navigation menu for switching between application views.
"""

from PyQt6.QtWidgets import QWidget

from ui.models import ModelContainer

from .helpers import (
    _add_title_and_icon,
    _create_layout,
    _create_menu_section,
    _set_active_menu_item,
    _setup_styles,
    _switch_to_config,
    _switch_to_overview,
    _switch_to_settings,
    _switch_to_strategies,
    _update_event_selection,
)


class NavigationMenu(QWidget):
    """Sidebar navigation menu for switching between application views."""

    _setup_styles = _setup_styles
    _create_layout = _create_layout
    _update_event_selection = _update_event_selection
    _add_title_and_icon = _add_title_and_icon
    _switch_to_overview = _switch_to_overview
    _switch_to_config = _switch_to_config
    _switch_to_strategies = _switch_to_strategies
    _switch_to_settings = _switch_to_settings
    _set_active_menu_item = _set_active_menu_item
    _create_menu_section = _create_menu_section

    def __init__(self, parent: QWidget, models: ModelContainer = None) -> None:
        super().__init__(parent)
        self.models = models
        self._menu_items: dict[type, object] = {}
        self._active_menu_item = None

        self._setup_styles()
        self._create_layout()

        if self.models and self.models.selection_model:
            self.models.selection_model.eventChanged.connect(self._update_event_selection)
            self.models.selection_model.sessionChanged.connect(self._update_event_selection)
