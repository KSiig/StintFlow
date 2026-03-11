"""Animated toggle switch widget with a sliding thumb."""

from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QSize, Qt, QVariantAnimation
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QAbstractButton, QSizePolicy


class ToggleSwitch(QAbstractButton):
    """A compact animated switch control for boolean settings."""

    def __init__(self, parent=None) -> None:
        """Initialize the switch with default colors and animation."""
        super().__init__(parent)

        self.setObjectName("ToggleSwitch")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self._track_width = 38
        self._track_height = 22
        self._thumb_margin = 3
        self._thumb_diameter = self._track_height - (self._thumb_margin * 2)
        self._thumb_position = 0.0

        self._off_track_color = QColor("#445066")
        self._on_track_color = QColor("#07a14b")
        self._disabled_track_color = QColor("#2f3948")
        self._thumb_color = QColor("#f7fbff")
        self._border_color = QColor("#1e2937")

        self._animation = QVariantAnimation(self)
        self._animation.setDuration(180)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._animation.valueChanged.connect(self._on_animation_value_changed)
        self.toggled.connect(self._animate_thumb)

    def sizeHint(self) -> QSize:  # type: ignore[override]
        """Return the preferred size for layout calculations."""
        return QSize(self._track_width, self._track_height)

    def paintEvent(self, event) -> None:  # type: ignore[override]
        """Draw the track and animated thumb."""
        _ = event

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(Qt.PenStyle.NoPen)

        track_color = self._track_color()
        painter.setBrush(track_color)
        painter.drawRoundedRect(0, 0, self._track_width, self._track_height, self._track_height / 2, self._track_height / 2)

        painter.setPen(self._border_color)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(0, 0, self._track_width, self._track_height, self._track_height / 2, self._track_height / 2)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._thumb_color)
        painter.drawEllipse(
            int(self._thumb_x_position()),
            self._thumb_margin,
            self._thumb_diameter,
            self._thumb_diameter,
        )

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        """Keep the fixed visual dimensions when layouts resize the widget."""
        super().resizeEvent(event)
        self.setFixedSize(self.sizeHint())

    def _animate_thumb(self, checked: bool) -> None:
        """Animate the thumb toward the checked or unchecked position."""
        start_value = self._thumb_position
        end_value = 1.0 if checked else 0.0

        self._animation.stop()
        self._animation.setStartValue(start_value)
        self._animation.setEndValue(end_value)
        self._animation.start()

    def _on_animation_value_changed(self, value) -> None:
        """Store the current animation value and repaint the switch."""
        self._thumb_position = float(value)
        self.update()

    def _thumb_x_position(self) -> float:
        """Return the animated x-position of the thumb within the track."""
        max_offset = self._track_width - self._thumb_diameter - (self._thumb_margin * 2)
        return self._thumb_margin + (max_offset * self._thumb_position)

    def _track_color(self) -> QColor:
        """Return the current track color for enabled and checked state."""
        if not self.isEnabled():
            return self._disabled_track_color
        return self._on_track_color if self.isChecked() else self._off_track_color