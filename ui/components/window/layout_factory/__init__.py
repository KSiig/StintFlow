"""Factory functions for assembling window layouts."""

from .create_scroll_area import create_scroll_area
from .create_stacked_container import create_stacked_container
from .create_right_pane import create_right_pane
from .create_main_layout import create_main_layout

__all__ = [
    "create_scroll_area",
    "create_stacked_container",
    "create_right_pane",
    "create_main_layout",
]
