"""Mirror tracking button appearance from config_options."""

from __future__ import annotations


def _apply_tracking_state(self, is_running: bool) -> None:
    """Update tracking button text and icon to match the running state."""
    source_btn = self.config_options.stop_btn if is_running else self.config_options.start_btn
    self.tracking_btn.setText(source_btn.text())
    self.tracking_btn.setIcon(source_btn.icon())
