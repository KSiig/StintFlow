from __future__ import annotations

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout

from ui.components.common.ConfigButton import ConfigButton
from ui.components.common.SectionHeader.SectionHeader import SectionHeader
from ui.components.stint_tracking.config import ConfigLabels


def _setup_ui(self) -> None:
    """Set up the strategy settings layout and controls."""
    layout = QVBoxLayout(self)

    frame = QFrame(self)
    frame.setObjectName("StrategySettingsFrame")
    frame.setFrameShape(QFrame.Shape.StyledPanel)
    frame.setFrameShadow(QFrame.Shadow.Raised)

    frame_layout = QVBoxLayout(frame)
    header = SectionHeader(
        title="Strategy Settings",
        icon_path="resources/icons/race_config/settings.svg",
        icon_color="#05fd7e",
        icon_size=20,
        spacing=8,
    )
    header.setObjectName("StrategySettingsHeader")
    frame_layout.setContentsMargins(4, 8, 4, 8)
    frame_layout.setSpacing(12)
    frame_layout.addWidget(header)

    btn_row = QHBoxLayout()
    self.edit_btn = ConfigButton(
        ConfigLabels.BTN_EDIT,
        icon_path="resources/icons/race_config/square-pen.svg",
        width="content",
    )
    self.save_btn = ConfigButton(
        ConfigLabels.BTN_SAVE,
        icon_path="resources/icons/race_config/square-pen.svg",
        width="content",
    )
    self.save_btn.hide()
    self.edit_btn.clicked.connect(self._toggle_edit)
    self.save_btn.clicked.connect(self._on_save_clicked)

    self.delete_btn = ConfigButton(
        "",
        icon_path="resources/icons/race_config/trash.svg",
        width="content",
        icon_color="#ff7070",
    )
    self.delete_btn.clicked.connect(self._on_delete_clicked)

    self._create_labeled_input_rows(frame_layout)
    self._set_inputs()

    frame_layout.addStretch()

    btn_row.addWidget(self.edit_btn)
    btn_row.addWidget(self.save_btn)
    btn_row.addStretch()
    btn_row.addWidget(self.delete_btn)
    frame_layout.addLayout(btn_row)

    frame.setLayout(frame_layout)

    layout.addWidget(frame)
    layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(layout)
