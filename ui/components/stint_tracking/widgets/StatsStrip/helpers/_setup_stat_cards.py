"""Create and wire stat cards for the StatsStrip content layout."""

from __future__ import annotations

from PyQt6.QtWidgets import QHBoxLayout

from ._get_avg_stint_time import _get_avg_stint_time
from ._get_longest_stint import _get_longest_stint
from ..StatsCard import StatsCard


def _setup_stat_cards(self, content_layout: QHBoxLayout) -> None:
    """Add stats cards to the provided content layout."""

    table_model = self.models.table_model

    self.avg_stint_time_card = StatsCard(
        title="Avg. Stint Time",
        value_text="Awaiting data",
        icon_path="resources/icons/stats_strip/timer.svg",
        icon_color="#39FF14",
        value_provider=_get_avg_stint_time,
    )
    self.avg_stint_time_card.refresh_value({"table_model": table_model})
    content_layout.addWidget(self.avg_stint_time_card)

    self.longest_stint_card = StatsCard(
        title="Longest Stint",
        value_text="Awaiting data",
        icon_path="resources/icons/stats_strip/trending-up.svg",
        icon_color="#a387f3",
        value_provider=_get_longest_stint,
    )
    self.longest_stint_card.refresh_value({"table_model": table_model})
    content_layout.addWidget(self.longest_stint_card)

    content_layout.addStretch()
