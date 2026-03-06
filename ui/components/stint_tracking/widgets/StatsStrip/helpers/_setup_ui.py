"""Build the StatsStrip layout."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QSizePolicy, QWidget
from ._get_avg_stint_time import _get_avg_stint_time

from ..StatsCard import StatsCard


def _setup_ui(self) -> None:
    """Create a horizontally scrollable strip with one stats card."""
    self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    outer = QHBoxLayout(self)
    outer.setContentsMargins(0, 0, 0, 0)

    frame = QFrame(self)
    frame.setObjectName("StatsStripFrame")
    frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    outer.addWidget(frame)

    frame_layout = QHBoxLayout(frame)
    frame_layout.setContentsMargins(0, 0, 0, 0)

    self.scroll_area = QScrollArea(frame)
    self.scroll_area.setObjectName("StatsStripScrollArea")
    self.scroll_area.setWidgetResizable(False)
    self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
    self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    self._content = QWidget(self.scroll_area)
    self._content.setObjectName("StatsStripContent")
    self._content.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

    content_layout = QHBoxLayout(self._content)
    content_layout.setContentsMargins(12, 8, 12, 8)
    content_layout.setSpacing(12)

    self.sample_stats_card = StatsCard(
        title="Placeholder Stat",
        value_text="Awaiting data",
        icon_path="resources/icons/table_headers/timer.svg",
        value_provider=_get_avg_stint_time,
    )
    self.sample_stats_card.refresh_value({"table_model": self.models.table_model})
    content_layout.addWidget(self.sample_stats_card)
    content_layout.addStretch()

    self._content.adjustSize()
    self.scroll_area.setWidget(self._content)
    frame_layout.addWidget(self.scroll_area)
