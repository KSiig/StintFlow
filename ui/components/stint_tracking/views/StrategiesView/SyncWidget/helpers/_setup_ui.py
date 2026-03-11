"""Build the SyncWidget UI."""

from __future__ import annotations

from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy, QVBoxLayout

from ._create_auto_sync_frame import _create_auto_sync_frame
from ._create_last_sync_label import _create_last_sync_label
from ._create_manual_sync_frame import _create_manual_sync_frame


def _setup_ui(self) -> None:
    """Create the sync button layout and styling hooks."""
    self.setObjectName("SyncWidget")
    self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

    outer_layout = QVBoxLayout(self)
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer_layout.setSpacing(8)

    bottom_row_layout = QHBoxLayout()
    bottom_row_layout.setContentsMargins(0, 0, 0, 0)
    bottom_row_layout.setSpacing(8)

    self.auto_sync_frame = _create_auto_sync_frame(self)
    self.manual_sync_frame = _create_manual_sync_frame(self)
    self.last_sync_label = _create_last_sync_label(self)

    bottom_row_layout.addWidget(self.auto_sync_frame)
    bottom_row_layout.addWidget(self.manual_sync_frame)

    outer_layout.addWidget(self.last_sync_label)
    outer_layout.addLayout(bottom_row_layout)