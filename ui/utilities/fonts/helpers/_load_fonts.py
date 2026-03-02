"""Load application fonts from disk once."""

from PyQt6.QtGui import QFontDatabase

from core.errors import log
from core.utilities import resource_path
from ui.utilities.fonts import _state


def _load_fonts() -> None:
    """Load the WorkSans font family and stash the family name."""
    if _state.font_family:
        return

    font_id = QFontDatabase.addApplicationFont(
        resource_path("resources/fonts/WorkSans-VariableFont_wght.ttf")
    )
    if font_id == -1:
        log(
            "ERROR",
            "Failed to load font WorkSans, falling back to Sans Serif",
            category="ui",
            action="load_fonts",
        )
        _state.font_family = "Sans Serif"
        return

    font_families = QFontDatabase.applicationFontFamilies(font_id)
    if font_families:
        log("INFO", "Font family loaded successfully", category="ui", action="load_fonts")
        _state.font_family = font_families[0]
    else:
        log(
            "ERROR",
            "Font loaded but no families returned, falling back to Sans Serif",
            category="ui",
            action="load_fonts",
        )
        _state.font_family = "Sans Serif"
