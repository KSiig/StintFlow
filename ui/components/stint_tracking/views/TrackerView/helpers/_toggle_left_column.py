"""Toggle the left configuration column's visibility."""

from __future__ import annotations

from ui.components.stint_tracking.config.config_constants import ConfigLabels


def _toggle_left_column(self) -> None:
    """Show or hide the controls column."""
    container = getattr(self, "left_column_container", None)
    button = getattr(self, "_left_column_toggle_btn", None)
    if container is None or button is None:
        return

    currently_hidden = container.isHidden()
    container.setHidden(not currently_hidden)
    button.setText(
        ConfigLabels.BTN_HIDE_OPTIONS if currently_hidden else ConfigLabels.BTN_SHOW_OPTIONS
    )
    self._update_controls_width()
