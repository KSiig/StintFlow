"""Create and wire driver stat cards for the StatsStrip content layout."""

from PyQt6.QtWidgets import QHBoxLayout


def _setup_driver_stats(self, content_layout: QHBoxLayout) -> None:
    """Attach the driver stats section to the shared strip content layout."""
    self._driver_stats_layout = QHBoxLayout()
    self._driver_stats_layout.setContentsMargins(0, 0, 0, 0)
    self._driver_stats_layout.setSpacing(12)
    content_layout.addLayout(self._driver_stats_layout)

    self._refresh_driver_stats()
