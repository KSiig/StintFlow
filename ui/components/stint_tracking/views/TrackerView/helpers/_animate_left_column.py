"""Animate the TrackerView left column width."""

from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QVariantAnimation


def _animate_left_column(self, is_visible: bool, duration: int = 200) -> None:
    """Slide the left column open or closed over *duration* milliseconds."""
    container = getattr(self, 'left_column_container', None)
    if container is None:
        return

    current_animation = getattr(self, '_left_column_animation', None)
    if current_animation is not None:
        current_animation.stop()

    expanded_width = max(
        getattr(self, '_left_column_expanded_width', 0),
        container.sizeHint().width(),
    )
    self._left_column_expanded_width = expanded_width

    start_width = max(container.width(), container.maximumWidth(), 0)
    end_width = expanded_width if is_visible else 0

    if is_visible:
        container.setHidden(False)

    animation = QVariantAnimation(self)
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
    animation.setStartValue(start_width)
    animation.setEndValue(end_width)

    def _on_value_changed(value) -> None:
        width = int(value)
        container.setMinimumWidth(width)
        container.setMaximumWidth(width)
        self._update_controls_width()

    def _on_finished() -> None:
        final_width = expanded_width if is_visible else 0
        container.setMinimumWidth(final_width)
        container.setMaximumWidth(final_width)
        container.setHidden(not is_visible)
        self._left_column_animation = None
        self._update_controls_width()

    animation.valueChanged.connect(_on_value_changed)
    animation.finished.connect(_on_finished)

    self._left_column_animation = animation
    animation.start()