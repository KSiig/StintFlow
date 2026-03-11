"""Update the auto-sync icon to reflect the current state."""

from __future__ import annotations

from ui.utilities.load_icon import load_icon


def _update_auto_sync_icon(self, enabled: bool) -> None:
    """Swap the auto-sync icon and color for enabled and disabled states."""
    if self.auto_sync_icon_label is None:
        return

    icon_path = "resources/icons/strategies/wifi.svg" if enabled else "resources/icons/strategies/wifi-off.svg"
    icon_color = "#07a14b" if enabled else "#506079"
    self.auto_sync_icon_label.setPixmap(load_icon(icon_path, 14, color=icon_color))