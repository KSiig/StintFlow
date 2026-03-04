from __future__ import annotations

from datetime import datetime, timedelta

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor, QPainter, QPolygon
from PyQt6.QtWidgets import QFrame


def _paint_event(self, event) -> None:
    """Paint a status triangle when heartbeat staleness exceeds thresholds."""
    QFrame.paintEvent(self, event)

    heartbeat_dt = getattr(self, 'heartbeat_dt', None)
    if not isinstance(heartbeat_dt, datetime):
        return

    age = datetime.now(heartbeat_dt.tzinfo) - heartbeat_dt
    if age > timedelta(minutes=5):
        color = '#FF3B30'
    elif age > timedelta(minutes=1):
        color = '#FF9500'
    else:
        return

    painter = QPainter(self)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(color))

    size = 10
    triangle = QPolygon([QPoint(0, 0), QPoint(size, 0), QPoint(0, size)])
    painter.drawPolygon(triangle)
    painter.end()
