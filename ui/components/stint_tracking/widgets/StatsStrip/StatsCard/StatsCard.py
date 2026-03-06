"""Reusable card widget used inside StatsStrip."""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtWidgets import QFrame

from .bounded_functions import _refresh_value, _setup_ui


class StatsCard(QFrame):
    """Single stat card with an icon/title row and a computed value row."""

    _setup_ui = _setup_ui
    refresh_value = _refresh_value

    def __init__(
        self,
        title: str,
        value_text: str = "—",
        icon_path: str = "resources/icons/table_headers/timer.svg",
        icon_color: str = "#D1D5DC",
        value_provider: Callable = None,
    ) -> None:
        super().__init__()
        self.setObjectName("StatsCard")

        self.title = title
        self.value_text = value_text
        self.icon_path = icon_path
        self.icon_color = icon_color
        self.value_provider = value_provider

        self.icon_label = None
        self.title_label = None
        self.value_label = None

        self._setup_ui()
