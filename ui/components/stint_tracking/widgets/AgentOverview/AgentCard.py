from __future__ import annotations

from datetime import datetime, timedelta

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor, QPainter, QPolygon
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout

from core.errors import log_exception
from ui.utilities import FONT, get_fonts


def _format_ts(val):
    if isinstance(val, datetime):
        ts = val
    else:
        try:
            ts = datetime.fromisoformat(str(val))
        except Exception:
            return str(val)
    if ts.tzinfo is None:
        from datetime import timezone

        ts = ts.replace(tzinfo=timezone.utc)
    try:
        ts = ts.astimezone()
    except Exception:
        pass
    age = datetime.now(ts.tzinfo) - ts
    if age > timedelta(days=1):
        return ts.strftime("%d-%m/%y %H:%M")
    return ts.strftime("%H:%M")


class AgentCard(QFrame):
    """Card showing a single agent's details."""

    def __init__(self, agent: dict) -> None:
        super().__init__()
        self.setObjectName('AgentCard')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(2)

        heartbeat_dt = None
        for field in ['name', 'connected_at', 'last_heartbeat']:
            if field not in agent:
                log_exception(
                    ValueError(f'Missing expected field "{field}" in agent document'),
                    f'Agent document missing "{field}"',
                    category='agent_overview',
                    action='render_agent_card',
                )
            raw = agent.get(field, 'N/A')
            value = raw
            if field in ('connected_at', 'last_heartbeat') and raw != 'N/A':
                value = _format_ts(raw)
                if field == 'last_heartbeat':
                    try:
                        parsed = datetime.fromisoformat(str(raw))
                    except Exception:
                        parsed = None
                    if parsed is not None:
                        if parsed.tzinfo is None:
                            from datetime import timezone

                            parsed = parsed.replace(tzinfo=timezone.utc)
                        try:
                            parsed = parsed.astimezone()
                        except Exception:
                            pass
                        heartbeat_dt = parsed
            lbl = QLabel(f"{field.capitalize()}: {value}")
            lbl.setFont(get_fonts(FONT.input_lbl))
            if field in ('connected_at', 'last_heartbeat') and raw != 'N/A':
                lbl.setToolTip(str(raw))
            layout.addWidget(lbl)
        self.heartbeat_dt = heartbeat_dt

    def paintEvent(self, event):
        super().paintEvent(event)
        dt = getattr(self, 'heartbeat_dt', None)
        if not isinstance(dt, datetime):
            return
        age = datetime.now(dt.tzinfo) - dt
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
        p1 = QPoint(0, 0)
        p2 = QPoint(size, 0)
        p3 = QPoint(0, size)
        painter.drawPolygon(QPolygon([p1, p2, p3]))
        painter.end()
