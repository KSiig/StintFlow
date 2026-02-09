"""
Window resize controller for frameless windows.

Handles edge and corner resizing for frameless PyQt6 windows,
including cursor updates and resize geometry calculations.
"""

from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtWidgets import QMainWindow


class ResizeController:
    """
    Manages edge and corner resizing for frameless windows.
    
    Tracks resize state, updates cursor based on edge proximity,
    and calculates new window geometry during resize operations.
    """
    
    def __init__(self, window: QMainWindow, edge_margin: int = 8):
        """
        Initialize the resize controller.
        
        Args:
            window: The window to control resizing for
            edge_margin: Pixel distance from edge to trigger resize (default: 8)
        """
        self.window = window
        self.edge_margin = edge_margin
        
        # Resize state tracking
        self._resize_start_pos: QPoint | None = None
        self._resize_start_geometry: QRect | None = None
        self._resize_edge: str | None = None  # 'left', 'right', 'bottom', etc.
    
    def get_resize_edge(self, pos: QPoint) -> str | None:
        """
        Determine which edge or corner of the window the mouse is near.
        
        Args:
            pos: Mouse position relative to the window
            
        Returns:
            Edge/corner name ('left', 'right', 'bottom', 'bottom-left', 'bottom-right')
            or None if not near an edge/corner or if window is maximized
        """
        # Disable resize detection when window is maximized
        if self.window.isMaximized():
            return None
        
        rect = self.window.rect()
        
        at_left = pos.x() <= self.edge_margin
        at_right = pos.x() >= rect.width() - self.edge_margin
        at_bottom = pos.y() >= rect.height() - self.edge_margin
        
        # Check corners first (they take priority over edges)
        if at_bottom and at_left:
            return 'bottom-left'
        if at_bottom and at_right:
            return 'bottom-right'
        
        # Check edges
        if at_left:
            return 'left'
        if at_right:
            return 'right'
        if at_bottom:
            return 'bottom'
        
        return None
    
    def update_cursor(self, edge: str | None = None) -> None:
        """
        Update the mouse cursor based on which edge or corner is being hovered.
        
        Args:
            edge: Edge/corner name ('left', 'right', 'bottom', 'bottom-left', 'bottom-right')
                  or None to reset to default cursor
        """
        if edge == 'bottom-left':
            self.window.setCursor(Qt.CursorShape.SizeBDiagCursor)  # ↙↗ diagonal
        elif edge == 'bottom-right':
            self.window.setCursor(Qt.CursorShape.SizeFDiagCursor)  # ↘↖ diagonal
        elif edge == 'left' or edge == 'right':
            self.window.setCursor(Qt.CursorShape.SizeHorCursor)  # ↔ horizontal
        elif edge == 'bottom':
            self.window.setCursor(Qt.CursorShape.SizeVerCursor)  # ↕ vertical
        else:
            self.window.setCursor(Qt.CursorShape.ArrowCursor)
    
    def start_resize(self, edge: str, global_pos: QPoint) -> None:
        """
        Start a resize operation from the specified edge.
        
        Args:
            edge: Edge/corner to resize from
            global_pos: Global mouse position when resize started
        """
        self._resize_edge = edge
        self._resize_start_pos = global_pos
        self._resize_start_geometry = self.window.geometry()
    
    def is_resizing(self) -> bool:
        """
        Check if a resize operation is currently in progress.
        
        Returns:
            True if resizing, False otherwise
        """
        return self._resize_start_pos is not None
    
    def update_resize(self, global_pos: QPoint) -> None:
        """
        Update the window geometry during a resize operation.
        
        Args:
            global_pos: Current global mouse position
        """
        if not self.is_resizing():
            return
        
        delta = global_pos - self._resize_start_pos
        new_geometry = QRect(self._resize_start_geometry)
        
        if self._resize_edge == 'left':
            # Resize from left edge
            new_geometry.setLeft(self._resize_start_geometry.left() + delta.x())
        elif self._resize_edge == 'right':
            # Resize from right edge
            new_geometry.setRight(self._resize_start_geometry.right() + delta.x())
        elif self._resize_edge == 'bottom':
            # Resize from bottom edge
            new_geometry.setBottom(self._resize_start_geometry.bottom() + delta.y())
        elif self._resize_edge == 'bottom-left':
            # Resize from bottom-left corner
            new_geometry.setLeft(self._resize_start_geometry.left() + delta.x())
            new_geometry.setBottom(self._resize_start_geometry.bottom() + delta.y())
        elif self._resize_edge == 'bottom-right':
            # Resize from bottom-right corner
            new_geometry.setRight(self._resize_start_geometry.right() + delta.x())
            new_geometry.setBottom(self._resize_start_geometry.bottom() + delta.y())
        
        self.window.setGeometry(new_geometry)
    
    def stop_resize(self) -> None:
        """Stop the current resize operation and clear resize state."""
        self._resize_edge = None
        self._resize_start_pos = None
        self._resize_start_geometry = None
