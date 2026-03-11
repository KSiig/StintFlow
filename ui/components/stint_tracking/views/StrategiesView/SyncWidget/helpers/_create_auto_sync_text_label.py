"""Build the text label for the auto-sync control."""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QWidget


def _create_auto_sync_text_label(parent: QWidget) -> QLabel:
    """Return the descriptive label for the auto-sync toggle."""
    label = QLabel("Auto-sync", parent)
    label.setObjectName("AutoSyncText")
    return label
