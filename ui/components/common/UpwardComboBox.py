"""
ComboBox that opens its dropdown above instead of below.

Useful for UI elements positioned at the bottom of the screen where
a downward dropdown would be clipped or extend off-screen.
"""

from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import QPoint


class UpwardComboBox(QComboBox):
    """
    ComboBox that opens its dropdown above instead of below.
    
    Overrides the default behavior to position the popup menu above
    the combo box instead of below it.
    """
    
    def showPopup(self) -> None:
        """
        Override to show popup above the combo box.
        
        Calculates the popup position to appear above the combo box
        while maintaining the same horizontal alignment.
        """
        super().showPopup()
        popup = self.view().parentWidget()
        
        if popup:
            # Get combo box position and size
            combo_pos = self.mapToGlobal(QPoint(0, 0))
            popup_height = popup.height()
            
            # Position popup above the combo box
            popup.move(combo_pos.x(), combo_pos.y() - popup_height)
