"""Typography definitions for the application UI."""

from enum import Enum
from PyQt6.QtGui import QFont


class FONT(Enum):
    """Typography definitions for different UI elements."""
    text_micro = {"point_size": 6.75, "weight": QFont.Weight.Normal}
    text_caption = {"point_size": 7.5, "weight": QFont.Weight.Normal}
    text_label = {"point_size": 9, "weight": QFont.Weight.Medium}
    text_label_bold = {"point_size": 9, "weight": QFont.Weight.DemiBold}
    text_body_sm = {"point_size": 9.75, "weight": QFont.Weight.Normal}
    text_body = {"point_size": 10.5, "weight": QFont.Weight.Normal}
    text_body_bold = {"point_size": 10.5, "weight": QFont.Weight.DemiBold}
    text_ui = {"point_size": 12, "weight": QFont.Weight.Medium}
    text_ui_bold = {"point_size": 12, "weight": QFont.Weight.DemiBold}
    text_title_sm = {"point_size": 13.5, "weight": QFont.Weight.DemiBold}
    text_title = {"point_size": 15, "weight": QFont.Weight.DemiBold}
    text_heading = {"point_size": 18, "weight": QFont.Weight.DemiBold}
    text_display = {"point_size": 24, "weight": QFont.Weight.DemiBold}

    font_regular = {"point_size": 10.5, "weight": QFont.Weight.Normal}
    font_medium = {"point_size": 10.5, "weight": QFont.Weight.Medium}
    font_semibold = {"point_size": 10.5, "weight": QFont.Weight.DemiBold}
    font_bold = {"point_size": 10.5, "weight": QFont.Weight.Bold}

    title = {"point_size": 15, "weight": QFont.Weight.DemiBold}
    header_nav = {"point_size": 14, "weight": QFont.Weight.DemiBold}
    header_table = {"point_size": 12, "weight": QFont.Weight.DemiBold}
    header_input = {"point_size": 12, "weight": QFont.Weight.DemiBold}
    menu_section = {"point_size": 10.5, "weight": QFont.Weight.DemiBold}
    combo_input = {"point_size": 10.5, "weight": QFont.Weight.Normal}
    text_small = {"point_size": 12, "weight": QFont.Weight.Medium}
    text_table_cell = {"point_size": 10, "weight": QFont.Weight.Normal}
    header_input_hint = {"point_size": 8, "weight": QFont.Weight.Normal}

    table_header = {"point_size": 10.5, "weight": QFont.Weight.DemiBold}
    table_cell = {"point_size": 10.5, "weight": QFont.Weight.Normal}

    dialog_header = {"point_size": 12, "weight": QFont.Weight.DemiBold}
    dialog_msg = {"point_size": 10.5, "weight": QFont.Weight.Normal}

    input_lbl = {"point_size": 9, "weight": QFont.Weight.Normal}
    input_field = dialog_msg