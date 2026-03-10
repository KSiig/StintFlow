"""Create the manual sync button frame."""

from __future__ import annotations

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy

from ui.utilities.load_icon import load_icon


def _create_manual_sync_frame(self) -> QFrame:
    """Return the clickable frame used to trigger immediate sync."""
    frame = QFrame(self)
    frame.setObjectName("SyncFrame")
    frame.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    frame.setCursor(Qt.CursorShape.PointingHandCursor)

    layout = QHBoxLayout(frame)
    layout.setContentsMargins(12, 8, 12, 8)
    layout.setSpacing(8)

    self.icon_label = QLabel(frame)
    self.icon_label.setObjectName("SyncIcon")
    self.icon_label.setPixmap(load_icon("resources/icons/strategies/refresh-ccw.svg", 14, color="#FFFFFF"))
    self.icon_label.setFixedSize(QSize(14, 14))

    self.text_label = QLabel("Sync now", frame)
    self.text_label.setObjectName("SyncText")

    layout.addWidget(self.icon_label)
    layout.addWidget(self.text_label)

    def _emit_sync_request(event) -> None:
        QFrame.mousePressEvent(frame, event)
        self.sync_requested.emit()

    frame.mousePressEvent = _emit_sync_request
    return frame