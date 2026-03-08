"""Create and wire stat cards for the StatsStrip content layout."""

from __future__ import annotations

from PyQt6.QtWidgets import QHBoxLayout

from ._get_avg_stint_time import _get_avg_stint_time
from ._get_longest_stint import _get_longest_stint
from ._get_stints_done import _get_stints_done
from ._get_tires_left import _get_tires_left
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
    content_layout.addWidget(self.avg_stint_time_card)

    self.longest_stint_card = StatsCard(
        title="Longest Stint",
        value_text="Awaiting data",
        icon_path="resources/icons/stats_strip/trending-up.svg",
        icon_color="#a387f3",
        value_provider=_get_longest_stint,
    )
    content_layout.addWidget(self.longest_stint_card)

    self.stints_done_card = StatsCard(
        title="Stints done",
        value_text="Awaiting data",
        icon_path="resources/icons/stats_strip/flag.svg",
        icon_color="#5490d9",
        value_provider=_get_stints_done,
    )
    content_layout.addWidget(self.stints_done_card)

    self.tires_left_card = StatsCard(
        title="Tires left",
        value_text="Awaiting data",
        icon_path="resources/icons/stats_strip/layers.svg",
        icon_color="#f66f82",
        value_provider=_get_tires_left,
    )
    content_layout.addWidget(self.tires_left_card)

    self._set_values()
    table_model.editorsNeedRefresh.connect(self._set_values)
