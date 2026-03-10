"""Create the conditional last sync label for the sync widget."""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


def _create_last_sync_label(self) -> QLabel:
    """Create the label that displays the latest strategy sync time."""
    label = QLabel()
    label.setObjectName("LastSyncLabel")
    label.setFont(self.font_last_sync)
    label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    label.hide()
    return label