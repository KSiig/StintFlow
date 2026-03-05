from __future__ import annotations

from datetime import datetime, timezone

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

from core.errors import log_exception

from ..helpers import _format_ts


def _setup_ui(self, agent: dict) -> None:
    """Build two horizontal rows with name/status and connected/heartbeat timestamps."""
    heartbeat_dt = None
    expected_fields = ["name", "connected_at", "last_heartbeat"]

    for field in expected_fields:
        if field not in agent:
            log_exception(
                ValueError(f'Missing expected field "{field}" in agent document'),
                f'Agent document missing "{field}"',
                category='agent_overview',
                action='render_agent_card',
            )

    name_raw = agent.get('name', 'N/A')
    connected_raw = agent.get('connected_at', 'N/A')
    heartbeat_raw = agent.get('last_heartbeat', 'N/A')

    connected_display = connected_raw
    heartbeat_display = heartbeat_raw

    if connected_raw != 'N/A':
        connected_display = _format_ts(connected_raw)

    if heartbeat_raw != 'N/A':
        heartbeat_display = _format_ts(heartbeat_raw)
        try:
            parsed = datetime.fromisoformat(str(heartbeat_raw))
        except Exception:
            parsed = None

        if parsed is not None:
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            try:
                parsed = parsed.astimezone()
            except Exception:
                pass
            heartbeat_dt = parsed

    self._set_status_color(heartbeat_dt)

    layout = QVBoxLayout(self)
    layout.setContentsMargins(6, 6, 6, 6)
    layout.setSpacing(4)

    top_row = QHBoxLayout()
    top_row.setContentsMargins(0, 0, 0, 0)
    top_row.setSpacing(8)

    name_label = QLabel(name_raw)
    name_label.setFont(self.font_name)
    name_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    top_row.addWidget(name_label)

    status_label = QLabel(self.status_text)
    status_label.setFont(self.font_status)
    status_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    status_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    status_label.setStyleSheet(f"""
                               background-color: {self.status_color};
                               color: {self.font_color};
                               padding: 2px 4px 2px 4px;
                               border-radius: 4px;
                            """)
    top_row.addWidget(status_label)
    top_row.addStretch()

    bottom_row = QHBoxLayout()
    bottom_row.setContentsMargins(0, 0, 0, 0)
    bottom_row.setSpacing(12)

    connected_label = QLabel(f"Connected: {connected_display}")
    connected_label.setFont(self.font_timestamps)
    connected_label.setObjectName('ConnectedLabel')
    if connected_raw != 'N/A':
        connected_label.setToolTip(str(connected_raw))
    bottom_row.addWidget(connected_label)

    heartbeat_label = QLabel(f"Heartbeat: {heartbeat_display}")
    heartbeat_label.setFont(self.font_timestamps)
    heartbeat_label.setObjectName('HeartbeatLabel')
    if heartbeat_raw != 'N/A':
        heartbeat_label.setToolTip(str(heartbeat_raw))
    bottom_row.addWidget(heartbeat_label)
    bottom_row.addStretch()

    layout.addLayout(top_row)
    layout.addLayout(bottom_row)

    self.heartbeat_dt = heartbeat_dt
