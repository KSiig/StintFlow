from enum import Enum
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from helpers import resource_path

class FONT(Enum):
  title = {
    "point_size": 16,
    "weight": QFont.Weight.DemiBold
  }
  small_text = {
    "point_size": 12,
    "weight": QFont.Weight.DemiBold
  }

def get_fonts(typography):
  font_id = QFontDatabase.addApplicationFont(resource_path('fonts\\Inter-VariableFont_opsz,wght.ttf'))
  if font_id == -1:
      print("Failed to load font Inter")
  else:
      # Get the family name
      font_settings = typography.value
      font_families = QFontDatabase.applicationFontFamilies(font_id)
      print("Loaded font families:", font_families)
      font_family = font_families[0]

      font = QFont(font_family)
      font.setPointSize(font_settings['point_size'])
      font.setWeight(font_settings['weight'])
      font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
      font.setStyleStrategy(
          QFont.StyleStrategy.PreferAntialias |
          QFont.StyleStrategy.NoSubpixelAntialias
      )

      return font