"""Build the toggle switch used by the auto-sync control."""

from __future__ import annotations

from PyQt6.QtWidgets import QWidget

from ui.components.common import ToggleSwitch


def _create_auto_sync_toggle(parent: QWidget) -> ToggleSwitch:
    """Return a ready-to-use toggle switch for auto-sync."""
    toggle = ToggleSwitch(parent)
    toggle.setObjectName("AutoSyncToggle")
    toggle.setChecked(False)
    return toggle
