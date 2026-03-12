"""Toggle the left configuration column's visibility."""

from __future__ import annotations

from ui.components.stint_tracking.config.config_constants import ConfigLabels


def _toggle_left_column(self) -> None:
    """Show or hide the controls column."""
    container = getattr(self, "left_column_container", None)
    button = getattr(self, "_left_column_toggle_btn", None)
    if container is None or button is None:
        return

    target_visible = container.isHidden()
    button.setText(
        ConfigLabels.BTN_HIDE_OPTIONS if target_visible else ConfigLabels.BTN_SHOW_OPTIONS
    )

    if not self.isVisible():
        target_width = 0
        if target_visible:
            target_width = max(
                getattr(self, '_left_column_expanded_width', 0),
                container.sizeHint().width(),
            )
            self._left_column_expanded_width = target_width

        container.setMinimumWidth(target_width)
        container.setMaximumWidth(target_width)
        container.setHidden(not target_visible)
        self._update_controls_width()
        return

    self._animate_left_column(target_visible)
