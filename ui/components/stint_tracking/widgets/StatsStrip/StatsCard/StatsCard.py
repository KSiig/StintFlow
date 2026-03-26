"""Reusable card widget used inside StatsStrip."""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtWidgets import QFrame

from .bounded_functions import _refresh_value, _setup_ui
from ui.utilities.load_style import load_style
from ui.utilities import FONT, get_fonts


class StatsCard(QFrame):
    """Single stat card with an icon/title row and a computed value row."""

    _setup_ui = _setup_ui
    refresh_value = _refresh_value

    def __init__(
        self,
        title: str,
        value_text: str = "—",
        value_right_text: str = "",
        icon_path: str = "resources/icons/table_headers/timer.svg",
        icon_color: str = "#D1D5DC",
        value_provider: Callable = None,
    ) -> None:
        super().__init__()
        load_style('resources/styles/stint_tracking/tracker/stats_card.qss', widget=self)
        self.setObjectName("StatsCard")

        self.font_title = get_fonts(FONT.text_body)
        self.font_value = get_fonts(FONT.text_ui)

        self.title = title
        self.value_text = value_text
        self.value_right_text = value_right_text
        self.icon_path = icon_path
        self.icon_color = icon_color
        self.value_provider = value_provider

        self.icon_label = None
        self.title_label = None
        self.value_label = None
        self.value_right_label = None

        self._setup_ui()
