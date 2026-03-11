"""Build the icon label for the auto-sync control."""

from __future__ import annotations

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QLabel, QWidget

from ui.utilities.load_icon import load_icon


def _create_auto_sync_icon_label(parent: QWidget) -> QLabel:
    """Return the styled icon needed for the auto-sync frame."""
    label = QLabel(parent)
    label.setObjectName("AutoSyncIcon")
    label.setPixmap(load_icon("resources/icons/strategies/wifi-off.svg", 14, color="#506079"))
    label.setFixedSize(QSize(14, 14))
    return label
