from enum import Enum
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from helpers import resource_path

font_family = None

class FONT(Enum):
  title = {
    "point_size": 16,
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
    "point_size": 8,
    "weight": QFont.Weight.Normal
  }
  text_small = {
    "point_size": 12,
    "weight": QFont.Weight.Medium
  }

def get_fonts(typography):
    global font_family

    load_fonts()

    font_settings = typography.value
    font = QFont(font_family)
    font.setPointSize(font_settings['point_size'])
    font.setWeight(font_settings['weight'])
    font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
    font.setStyleStrategy(
        QFont.StyleStrategy.PreferAntialias |
        QFont.StyleStrategy.NoSubpixelAntialias
    )

    return font

def load_fonts():
  global font_family
  if not font_family:
    font_id = QFontDatabase.addApplicationFont(resource_path('fonts\\Inter-VariableFont_opsz,wght.ttf'))
    if font_id == -1:
        print("Failed to load font Inter")
    else:
        # Get the family name
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        print("Loaded font families:", font_families)
        font_family = font_families[0]