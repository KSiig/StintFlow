"""Create QFont instances with consistent styling."""

from PyQt6.QtGui import QFont

from ui.utilities.fonts import _state
from ui.utilities.fonts.font_definitions import FONT
from ui.utilities.fonts.helpers._load_fonts import _load_fonts


def get_fonts(typography: FONT) -> QFont:
    """Return a configured QFont for the given typography enum."""
    _load_fonts()

    font_settings = typography.value
    font = QFont(_state.font_family)
    font.setPointSizeF(font_settings["point_size"])
    font.setWeight(font_settings["weight"])
    font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
    font.setStyleStrategy(
        QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.NoSubpixelAntialias
    )

    return font
