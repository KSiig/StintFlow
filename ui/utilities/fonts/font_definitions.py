"""Typography definitions for the application UI."""

from enum import Enum
from PyQt6.QtGui import QFont


class FONT(Enum):
    """Typography definitions for different UI elements."""

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
