"""Create the conditional last sync label for the sync widget."""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


def _create_last_sync_label(self) -> QLabel:
    """Create the label that displays the latest strategy sync time."""
    from PyQt6.QtWidgets import QGraphicsOpacityEffect

    label = QLabel()
    label.setObjectName("LastSyncLabel")
    label.setFont(self.font_last_sync)
    label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    # reserve vertical space equal to one line of text so layout doesn't shift
    fm = label.fontMetrics()
    label.setFixedHeight(fm.height())
    # use opacity effect to hide text instead of removing label from layout
    opacity = QGraphicsOpacityEffect(label)
    opacity.setOpacity(0.0)
    label.setGraphicsEffect(opacity)
    label.setText("")
    return label