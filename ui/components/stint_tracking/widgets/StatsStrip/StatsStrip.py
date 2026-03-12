"""Horizontal stats strip shown between controls and stint table."""

from PyQt6.QtWidgets import QWidget

from ui.models import ModelContainer
from .helpers import (
    _install_hover_listener,
    _refresh_driver_stats,
    _fade_scrollbar,
    _set_scrollbar_visibility,
    _setup_driver_stats,
    _setup_stat_cards,
    _setup_ui,
    _set_values,
    _sync_scrollbar_visibility,
)
from ui.utilities.load_style import load_style


class StatsStrip(QWidget):
    """Scrollable strip for presenting session and stint statistics."""

    _install_hover_listener = _install_hover_listener
    _refresh_driver_stats = _refresh_driver_stats
    _fade_scrollbar = _fade_scrollbar
    _set_scrollbar_visibility = _set_scrollbar_visibility
    _setup_driver_stats = _setup_driver_stats
    _setup_ui = _setup_ui
    _setup_stat_cards = _setup_stat_cards
    _sync_scrollbar_visibility = _sync_scrollbar_visibility
    _set_values = _set_values

    def __init__(self, models: ModelContainer) -> None:
        super().__init__()
        load_style('resources/styles/stint_tracking/tracker/stats_strip.qss', widget=self)
        self.models = models
        self.scroll_area = None
        self._frame = None
        self._content = None
        self._driver_stats_layout = None
        self._hover_filter = None
        self.driver_stat_cards = []
        self.sample_stats_card = None
        self._setup_ui()
