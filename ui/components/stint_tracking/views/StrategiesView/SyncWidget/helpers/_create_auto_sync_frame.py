"""Create the auto-sync controls frame."""

from __future__ import annotations

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy

from ._create_auto_sync_icon_label import _create_auto_sync_icon_label
from ._create_auto_sync_text_label import _create_auto_sync_text_label
from ._create_auto_sync_toggle import _create_auto_sync_toggle


def _create_auto_sync_frame(self) -> QFrame:
    """Return the frame containing auto-sync icon, label, and toggle."""
    frame = QFrame(self)
    frame.setObjectName("AutoSyncFrame")
    frame.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    layout = QHBoxLayout(frame)
    layout.setContentsMargins(12, 8, 12, 8)
    layout.setSpacing(4)

    self.auto_sync_icon_label = _create_auto_sync_icon_label(frame)
    self.auto_sync_text_label = _create_auto_sync_text_label(frame)
    self.auto_sync_toggle = _create_auto_sync_toggle(frame)
    self.auto_sync_toggle.toggled.connect(self._handle_auto_sync_toggled)

    layout.addWidget(self.auto_sync_icon_label)
    layout.addWidget(self.auto_sync_text_label)
    layout.addWidget(self.auto_sync_toggle)

    return frame