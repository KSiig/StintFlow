from __future__ import annotations

from PyQt6.QtWidgets import QCheckBox, QLabel, QVBoxLayout

from ui.components.common import LabeledInputRow
from ui.components.stint_tracking.config.config_constants import ConfigLayout
from ui.components.stint_tracking.config import ConfigLabels
from ui.utilities import FONT, get_fonts
from ._on_text_changed import _on_text_changed


def _create_labeled_input_rows(self, layout: QVBoxLayout) -> None:
    """Create labeled inputs and lock checkbox for strategy settings."""
    for field_id, title in [
        ("name", "Strategy name"),
        ("mean_stint_time", "Mean stint time"),
    ]:
        card = LabeledInputRow(
            title=title,
            input_height=ConfigLayout.INPUT_HEIGHT,
        )
        card.textEditedByUser.connect(lambda _: _on_text_changed(self))
        self.inputs[field_id] = card.get_input_field()
        layout.addWidget(card)

    header = QLabel("Lock completed stints")
    try:
        header.setFont(get_fonts(FONT.header_input))
    except Exception:
        # Font loading failures are non-fatal; continue with default font.
        pass
    header.setObjectName("SettingTitle")
    layout.addWidget(header)

    lock_cb = QCheckBox()
    lock_cb.checkStateChanged.connect(lambda: _on_text_changed(self))
    self.inputs["lock_completed_stints"] = lock_cb
    layout.addWidget(lock_cb)
