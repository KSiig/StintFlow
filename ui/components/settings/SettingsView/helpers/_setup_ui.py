"""Compose the Settings view layout."""

from PyQt6.QtWidgets import QFrame, QVBoxLayout


def _setup_ui(self) -> None:
    """Build the settings UI layout."""
    frame = QFrame()
    frame.setObjectName("SettingsFrame")
    frame.setFixedWidth(512)

    root_layout = QVBoxLayout(self)
    root_layout.setContentsMargins(0, 0, 0, 0)
    root_layout.addWidget(frame)

    layout = QVBoxLayout(frame)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(16)

    self._build_agent_section(layout)
    self._build_mongo_section(layout)
    self._build_logging_section(layout)
    self._build_strategy_section(layout)
    self._build_status_section(layout)
    self._build_button_section(layout)
    layout.addStretch()
