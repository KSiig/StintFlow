"""
Draggable area widget for moving the main window.

An invisible overlay widget positioned absolutely at the top of the window
that allows users to click and drag to move the window. Does not participate
in any layout and doesn't affect other component positioning.
"""

from typing import Optional
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QMouseEvent


class DraggableArea(QWidget):
    """
    Invisible widget that enables window dragging when clicked.
    
    This widget is positioned absolutely at the top of the main window
    and captures mouse events to allow the user to move the frameless window.
    """
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._initial_pos: Optional[QPoint] = None
        self._was_maximized: bool = False  # Track if window was maximized when drag started
        
        # Make the widget invisible but still capture mouse events
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")
        
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Capture initial mouse position when user starts dragging.
        
        Args:
            event: Mouse press event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._initial_pos = event.position().toPoint()
            # Track if window is maximized when drag starts
            self._was_maximized = self.window().isMaximized()
        super().mousePressEvent(event)
        event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Move the window as the user drags.
        
        If the window was maximized when drag started, restore it to normal size
        and position it under the cursor (similar to most desktop applications).
        
        Args:
            event: Mouse move event
        """
        if self._initial_pos is not None:
            # If window was maximized, restore it first
            if self._was_maximized:
                # Get the global cursor position
                global_pos = event.globalPosition().toPoint()
                
                # Restore the window to normal size
                self.window().showNormal()
                
                # Calculate new position to center window under cursor
                # Use a ratio based on where the user clicked in the draggable area
                window_width = self.window().width()
                click_ratio = self._initial_pos.x() / self.width()
                offset_x = int(window_width * click_ratio)
                
                # Position window so cursor is at the same relative position
                new_x = global_pos.x() - offset_x
                new_y = global_pos.y() - self._initial_pos.y()
                
                self.window().move(new_x, new_y)
                
                # Update initial position to continue dragging from current position
                self._initial_pos = QPoint(offset_x, self._initial_pos.y())
                self._was_maximized = False
            else:
                # Normal dragging behavior
                delta = event.position().toPoint() - self._initial_pos
                self.window().move(
                    self.window().x() + delta.x(),
                    self.window().y() + delta.y(),
                )
        super().mouseMoveEvent(event)
        event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Reset position tracking when user releases mouse.
        
        Args:
            event: Mouse release event
        """
        self._initial_pos = None
        self._was_maximized = False
        super().mouseReleaseEvent(event)
        event.accept()
