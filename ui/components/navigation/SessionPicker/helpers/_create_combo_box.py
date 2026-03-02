"""Create a configured combo box for session picker."""

from PyQt6.QtWidgets import QSizePolicy

from ui.utilities import FONT, get_fonts
from ui.components.common import DataDropdownButton
from ...constants import COMBO_HEIGHT


def _create_combo_box(self) -> DataDropdownButton:
    """Create a configured DataDropdownButton with standard styling."""
    combo = DataDropdownButton()
    combo.setFont(get_fonts(FONT.combo_input))
    combo.set_text_alignment_left(padding_left=34)
    combo.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Fixed,
    )
    combo.setFixedHeight(COMBO_HEIGHT)
    return combo
