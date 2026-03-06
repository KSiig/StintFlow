"""Horizontal stats strip shown between controls and stint table."""

from PyQt6.QtWidgets import QWidget

from ui.models import ModelContainer
from .helpers import _setup_ui
from ui.utilities.load_style import load_style


class StatsStrip(QWidget):
    """Scrollable strip for presenting session and stint statistics."""

    _setup_ui = _setup_ui

    def __init__(self, models: ModelContainer) -> None:
        super().__init__()
        load_style('resources/styles/stint_tracking/config_options/stats_strip.qss', widget=self)
        self.models = models
        self.scroll_area = None
        self._content = None
        self.sample_stats_card = None
        self._setup_ui()
