from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QFrame, QVBoxLayout

from ui.components.common.SectionHeader.SectionHeader import SectionHeader
from ....config import ConfigLayout


def _setup_ui(self) -> None:
    """Build the configuration panel layout."""
    frame = QFrame()
    frame.setObjectName("ConfigOptions")
    frame.setFixedWidth(ConfigLayout.FRAME_WIDTH)

    root_widget_layout = QVBoxLayout(self)
    root_widget_layout.setContentsMargins(0, 0, 0, 0)
    root_widget_layout.addWidget(frame)

    self._create_buttons()

    root_layout = QVBoxLayout(frame)
    root_layout.setContentsMargins(0, 0, ConfigLayout.RIGHT_MARGIN, 0)
    root_layout.setSpacing(ConfigLayout.CONTENT_SPACING)

    header = SectionHeader(
        title="Race Configuration",
        icon_path="resources/icons/race_config/settings.svg",
        icon_color="#05fd7e",
        icon_size=ConfigLayout.ICON_SIZE,
        spacing=ConfigLayout.HEADER_SPACING,
    )
    root_layout.addWidget(header)

    self._add_config_rows(root_layout)
    root_layout.addLayout(self._create_button_layout())

    self.save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
    self.save_shortcut.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
    self.save_shortcut.activated.connect(self._handle_save_shortcut)

    self.save_btn.hide()
    root_layout.addStretch()
