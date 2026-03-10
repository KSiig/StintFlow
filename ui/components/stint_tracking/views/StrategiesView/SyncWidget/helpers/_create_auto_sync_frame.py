"""Create the auto-sync controls frame."""

from __future__ import annotations

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QSizePolicy

from ui.utilities.load_icon import load_icon


def _create_auto_sync_frame(self) -> QFrame:
    """Return the frame containing auto-sync icon, label, and toggle."""
    frame = QFrame(self)
    frame.setObjectName("AutoSyncFrame")
    frame.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    layout = QHBoxLayout(frame)
    layout.setContentsMargins(12, 8, 12, 8)
    layout.setSpacing(4)

    self.auto_sync_icon_label = QLabel(frame)
    self.auto_sync_icon_label.setObjectName("AutoSyncIcon")
    self.auto_sync_icon_label.setPixmap(load_icon("resources/icons/strategies/wifi-off.svg", 14, color="#506079"))
    self.auto_sync_icon_label.setFixedSize(QSize(14, 14))

    self.auto_sync_text_label = QLabel("Auto-sync", frame)
    self.auto_sync_text_label.setObjectName("AutoSyncText")

    self.auto_sync_toggle = QCheckBox(frame)
    self.auto_sync_toggle.setObjectName("AutoSyncToggle")
    self.auto_sync_toggle.setChecked(False)
    self.auto_sync_toggle.toggled.connect(self._handle_auto_sync_toggled)

    layout.addWidget(self.auto_sync_icon_label)
    layout.addWidget(self.auto_sync_text_label)
    layout.addWidget(self.auto_sync_toggle)

    return frame