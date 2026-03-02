"""Dataclass for navigation menu item configuration."""

from dataclasses import dataclass
from typing import Callable

from PyQt6.QtWidgets import QLabel, QWidget


@dataclass
class MenuItemConfig:
    """Configuration for a single navigation menu item."""

    label: str
    callback: Callable
    widget: QWidget
    window_class: type = None
    icon_path: str = None
    icon_label: QLabel = None
    is_active: bool = False
