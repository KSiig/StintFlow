"""
Font definitions and utilities for the application UI.

Provides a centralized FONT enum for typography definitions and the get_fonts()
function for creating QFont instances with consistent styling.
"""

from enum import Enum
from PyQt6.QtGui import QFontDatabase, QFont
from core.utilities import resource_path
from core.errors import log


font_family = None


class FONT(Enum):
    """Typography definitions for different UI elements."""
    title = {
        "point_size": 15,
        "weight": QFont.Weight.DemiBold
    }
    header_nav = {
        "point_size": 14,
        "weight": QFont.Weight.DemiBold
    }
    header_table = {
        "point_size": 12,
        "weight": QFont.Weight.DemiBold
    }
    header_input = {
        "point_size": 12,
        "weight": QFont.Weight.DemiBold
    }
    menu_section = {
        "point_size": 10.5,
        "weight": QFont.Weight.DemiBold
    }
    combo_input = {
        "point_size": 10.5,
        "weight": QFont.Weight.Normal
    }
    text_small = {
        "point_size": 12,
        "weight": QFont.Weight.Medium
    }
    text_table_cell = {
        "point_size": 10,
        "weight": QFont.Weight.Normal
    }
    header_input_hint = {
        "point_size": 8,
        "weight": QFont.Weight.Normal
    }

    ## Table fonts ##
    table_header = {
        "point_size": 10.5,
        "weight": QFont.Weight.DemiBold
    }
    table_cell = {
        "point_size": 10.5,
        "weight": QFont.Weight.Normal
    }

    ## Input fonts ##
    input_lbl = {
        "point_size": 9,
        "weight": QFont.Weight.Normal
    }
    input_field = {
        "point_size": 10.5,
        "weight": QFont.Weight.Normal
    }


def get_fonts(typography):
    """
    Create a QFont instance for the given typography definition.
    
    Args:
        typography (FONT): Typography enum value
        
    Returns:
        QFont: Configured font with styling applied
    """
    global font_family

    _load_fonts()

    font_settings = typography.value
    font = QFont(font_family)
    font.setPointSizeF(font_settings['point_size'])
    font.setWeight(font_settings['weight'])
    font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
    font.setStyleStrategy(
        QFont.StyleStrategy.PreferAntialias |
        QFont.StyleStrategy.NoSubpixelAntialias
    )

    return font


def _load_fonts():
    """
    Load application fonts from resources.

    Loads the WorkSans font family and sets the global font_family variable.
    Only loads once; subsequent calls are no-ops.
    """
    global font_family
    if not font_family:
        font_id = QFontDatabase.addApplicationFont(
            resource_path('resources/fonts/WorkSans-VariableFont_wght.ttf')
        )
        if font_id == -1:
            log('ERROR', 'Failed to load font WorkSans, falling back to Sans Serif', category='ui', action='load_fonts')
            font_family = 'Sans Serif'
        else:
            # Get the family name
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                log('INFO', 'Font family loaded successfully', category='ui', action='load_fonts')
                font_family = font_families[0]
            else:
                log('ERROR', 'Font loaded but no families returned, falling back to Sans Serif', category='ui', action='load_fonts')
                font_family = 'Sans Serif'
