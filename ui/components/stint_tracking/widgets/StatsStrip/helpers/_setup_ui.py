"""Build the StatsStrip layout."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QScrollArea, QSizePolicy, QWidget


def _setup_ui(self) -> None:
    """Create a horizontally scrollable strip with a placeholder label."""
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

    self.placeholder_label = QLabel("StatsStrip placeholder")
    self.placeholder_label.setObjectName("StatsStripPlaceholder")
    self.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
    content_layout.addWidget(self.placeholder_label)
    content_layout.addStretch()

    self._content.adjustSize()
    self.scroll_area.setWidget(self._content)
    frame_layout.addWidget(self.scroll_area)
