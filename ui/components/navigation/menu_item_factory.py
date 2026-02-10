"""
Menu item configuration and factory for navigation menu.

Provides dataclasses and factory functions for creating navigation menu items
with consistent styling and behavior.
"""

from dataclasses import dataclass
from typing import Callable

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

from ui.utilities import FONT, get_fonts, get_cached_icon
from ..common import ClickableWidget
from .constants import (
    MENU_SPACING,
    MENU_ITEM_ICON_SIZE,
    MENU_ITEM_ICON_COLOR,
    MENU_ITEM_ICON_COLOR_ACTIVE
)


@dataclass
class MenuItemConfig:
    """
    Configuration for a single navigation menu item.
    
    Encapsulates all data needed to render and track a menu item,
    reducing the need for multiple parallel tracking dictionaries.
    """
    label: str
    callback: Callable
    widget: QWidget
    window_class: type = None
    icon_path: str = None
    icon_label: QLabel = None
    is_active: bool = False


def create_menu_item(label: str, callback: Callable, icon_path: str = None, menu_spacing = MENU_SPACING * 2) -> MenuItemConfig:
    """
    Create a navigation menu item with optional icon.
    
    Factory function that creates a clickable menu item widget and returns
    a MenuItemConfig with all necessary tracking information.
    
    Args:
        label: Item label text
        callback: Function to call when item is clicked
        icon_path: Path to SVG icon file (optional, can be None for text-only items)
        
    Returns:
        MenuItemConfig with widget and tracking information
    """
    # Create clickable container
    container = ClickableWidget(callback)
    container.setObjectName("MenuItem")
    container.setProperty("active", False)
    
    icon_label_widget = None
    
    if icon_path:
        # Create layout with icon and label
        layout = QHBoxLayout()
        layout.setContentsMargins(menu_spacing, 8, 0, 8)
        layout.setSpacing(8)
        
        # Icon
        icon_label_widget = QLabel()
        icon_pixmap = get_cached_icon(icon_path, MENU_ITEM_ICON_SIZE, MENU_ITEM_ICON_COLOR)
        icon_label_widget.setPixmap(icon_pixmap)
        icon_label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label_widget)
        
        # Text label
        text_label = QLabel(label)
        text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        text_label.setFont(get_fonts(FONT.menu_section))
        layout.addWidget(text_label)
        layout.addStretch()
        
        container.setLayout(layout)
    else:
        # Simple text-only item
        item = QLabel(label)
        item.setFont(get_fonts(FONT.menu_section))
        layout = QHBoxLayout()
        layout.setContentsMargins(menu_spacing, 8, 0, 8)
        layout.addWidget(item)
        layout.addStretch()
        container.setLayout(layout)
    
    return MenuItemConfig(
        label=label,
        callback=callback,
        widget=container,
        icon_path=icon_path,
        icon_label=icon_label_widget
    )


def update_menu_item_state(item_config: MenuItemConfig, is_active: bool) -> None:
    """
    Update menu item's active state including visual styling and icon color.
    
    Handles both the widget property/style updates and icon color changes.
    Forces Qt to reapply stylesheets by unpolishing and polishing the widget tree.
    
    Args:
        item_config: Menu item configuration to update
        is_active: Whether the item should be styled as active
    """
    widget = item_config.widget
    
    # Update property and refresh styles
    widget.setProperty("active", is_active)
    _refresh_widget_style(widget)
    
    # Update icon color if item has an icon
    if item_config.icon_label and item_config.icon_path:
        icon_color = MENU_ITEM_ICON_COLOR_ACTIVE if is_active else MENU_ITEM_ICON_COLOR
        icon_pixmap = get_cached_icon(item_config.icon_path, MENU_ITEM_ICON_SIZE, icon_color)
        item_config.icon_label.setPixmap(icon_pixmap)
    
    # Update is_active flag
    item_config.is_active = is_active


def _refresh_widget_style(widget: QWidget) -> None:
    """
    Force Qt to reapply stylesheet to a widget and its children.
    
    Unpolishes and polishes the widget tree to ensure property-based
    selectors in QSS are re-evaluated.
    
    Args:
        widget: The widget to refresh
    """
    # Refresh all children first
    for child in widget.findChildren(QWidget):
        child.style().unpolish(child)
        child.style().polish(child)
    
    # Then refresh the widget itself
    widget.style().unpolish(widget)
    widget.style().polish(widget)
