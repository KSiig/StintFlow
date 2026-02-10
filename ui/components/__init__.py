"""
Barrel file for UI components.

Provides access to all UI components organized by category.
"""

from .common import ClickableWidget, UpwardComboBox, DraggableArea
from .window import ApplicationWindow, WindowButtons
from .navigation import NavigationMenu, SessionPicker, MenuItemConfig, create_menu_item, update_menu_item_state
from .stint_tracking import OverviewView, ConfigView
from .settings import SettingsView

__all__ = [
    # Common components
    'ClickableWidget',
    'UpwardComboBox',
    'DraggableArea',
    # Window components
    'ApplicationWindow',
    'WindowButtons',
    # Navigation components
    'NavigationMenu',
    'SessionPicker',
    'MenuItemConfig',
    'create_menu_item',
    'update_menu_item_state',
    # Stint tracking views
    'OverviewView',
    'ConfigView',
    # Settings views
    'SettingsView'
]
