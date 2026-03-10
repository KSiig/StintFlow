"""Build the SyncWidget UI."""

from __future__ import annotations

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QFrame

from ui.utilities.load_icon import load_icon


def _setup_ui(self) -> None:
    """Create the sync button layout and styling hooks."""
    self.setObjectName("SyncWidget")
    self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    # outer layout just holds the styled frame
    outer_layout = QHBoxLayout(self)
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer_layout.setSpacing(0)

    frame = QFrame(self)
    frame.setObjectName("SyncFrame")
    frame.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    layout = QHBoxLayout(frame)
    layout.setContentsMargins(12, 8, 12, 8)
    layout.setSpacing(0)

    outer_layout.addWidget(frame)

    # icon label
    self.icon_label = QLabel()
    self.icon_label.setObjectName("SyncIcon")
    self.icon_label.setPixmap(
        QIcon(load_icon("resources/icons/strategies/refresh-ccw.svg", 14, color="#FFFFFF")).pixmap(14, 14)
    )
    self.icon_label.setFixedSize(QSize(14, 14))

    # text label
    self.text_label = QLabel("Sync now")
    self.text_label.setObjectName("SyncText")

    layout.addWidget(self.icon_label)
    layout.addSpacing(8)
    layout.addWidget(self.text_label)