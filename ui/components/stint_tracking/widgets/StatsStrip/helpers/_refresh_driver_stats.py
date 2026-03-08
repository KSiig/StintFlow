"""Rebuild driver stat cards from current table data."""

from __future__ import annotations

from ..DriverStatCard import DriverStatCard

from ._clear_driver_stats_layout import _clear_driver_stats_layout
from ._get_driver_stats import _get_driver_stats


def _refresh_driver_stats(self) -> None:
    """Update driver stat cards from the latest model state."""
    driver_stats_layout = getattr(self, '_driver_stats_layout', None)
    if driver_stats_layout is None:
        return

    driver_stats = _get_driver_stats(self.models.table_model)

    if len(self.driver_stat_cards) != len(driver_stats):
        _clear_driver_stats_layout(driver_stats_layout)
        self.driver_stat_cards = []

        for driver_stat in driver_stats:
            driver_stat_card = DriverStatCard(
                driver_name=str(driver_stat['driver_name']),
                stint_count=int(driver_stat['stint_count']),
                total_time_text=str(driver_stat['total_time_text']),
                progress_value=int(driver_stat['progress_value']),
            )
            self.driver_stat_cards.append(driver_stat_card)
            driver_stats_layout.addWidget(driver_stat_card)

    for driver_stat_card, driver_stat in zip(self.driver_stat_cards, driver_stats):
        driver_stat_card.set_driver_stats(
            driver_name=str(driver_stat['driver_name']),
            stint_count=int(driver_stat['stint_count']),
            total_time_text=str(driver_stat['total_time_text']),
            progress_value=int(driver_stat['progress_value']),
        )

    content_widget = getattr(self, '_content', None)
    if content_widget is not None:
        content_widget.adjustSize()