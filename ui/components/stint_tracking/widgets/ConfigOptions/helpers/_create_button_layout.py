from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

from ....config import ConfigLayout


def _create_button_layout(self) -> QHBoxLayout:
    """Build layout containing action and tracking controls."""
    btn_layout = QVBoxLayout()
    btn_layout.setSpacing(ConfigLayout.BUTTON_SPACING)

    btn_layout_save_clone = QHBoxLayout()
    btn_layout_save_clone.addWidget(self.edit_btn, alignment=Qt.AlignmentFlag.AlignTop)
    btn_layout_save_clone.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignTop)
    btn_layout_save_clone.addWidget(self.clone_btn, alignment=Qt.AlignmentFlag.AlignTop)
    btn_layout_save_clone.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignTop)
    btn_layout_save_clone.addWidget(self.stop_btn, alignment=Qt.AlignmentFlag.AlignTop)

    btn_tracking_layout = QVBoxLayout()
    btn_tracking_layout.setSpacing(8)
    btn_tracking_layout.addWidget(self.create_session_btn, alignment=Qt.AlignmentFlag.AlignTop)
    btn_tracking_layout.addWidget(self.lbl_info, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
    btn_tracking_layout.addStretch()

    btn_layout.addWidget(self.practice_cb)
    btn_layout.addLayout(btn_layout_save_clone)
    btn_layout.addLayout(btn_tracking_layout)

    return btn_layout
