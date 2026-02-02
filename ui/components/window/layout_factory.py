"""
Layout factory for application window components.

Provides factory functions for creating window layouts and widget configurations.
Separates layout creation from window orchestration logic.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QScrollArea,
    QStackedLayout,
)
from PyQt6.QtCore import Qt

from .constants import WORKSPACE_MARGINS


def create_scroll_area() -> QScrollArea:
    """
    Create a scrollable content area for the main workspace.
    
    Returns:
        QScrollArea: Configured scroll area with no frame and auto-resize
    """
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setFrameShape(QFrame.Shape.NoFrame)
    
    return scroll_area


def create_stacked_container(scroll_area: QScrollArea) -> tuple[QWidget, QStackedLayout]:
    """
    Create a container with stacked layout for view switching.
    
    Args:
        scroll_area: The scroll area to contain the stacked layout
        
    Returns:
        Tuple of (container widget, stacked layout)
    """
    container = QWidget()
    layout = QStackedLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    
    scroll_area.setWidget(container)
    
    return container, layout


def create_right_pane(scroll_area: QScrollArea) -> QWidget:
    """
    Create the right pane containing the scrollable content area.
    
    Note: Window buttons are positioned absolutely, not included in this layout.
    
    Args:
        scroll_area: The scroll area to add to the pane
        
    Returns:
        QWidget: The configured right pane
    """
    pane = QWidget()
    layout = QVBoxLayout(pane)
    layout.setContentsMargins(WORKSPACE_MARGINS, 0, 0, WORKSPACE_MARGINS)
    layout.setSpacing(0)
    
    # Window buttons are positioned absolutely, not added to layout
    layout.addWidget(scroll_area)
    
    return pane


def create_main_layout(navigation_menu: QWidget, right_pane: QWidget) -> QFrame:
    """
    Create the main application layout with navigation and content panes.
    
    Creates a two-pane horizontal layout:
    - Left: Navigation menu (static)
    - Right: Content area with switchable views
    
    Args:
        navigation_menu: The navigation menu widget
        right_pane: The right pane widget containing content
        
    Returns:
        QFrame: Border frame containing the assembled layout
    """
    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(0, WORKSPACE_MARGINS, 0, 0)
    main_layout.setSpacing(0)
    
    # Left pane: Navigation menu (static)
    main_layout.addWidget(navigation_menu, alignment=Qt.AlignmentFlag.AlignLeft)
    
    # Right pane: Content area
    main_layout.addWidget(right_pane)
    
    # Border frame to wrap everything
    border_frame = QFrame()
    border_frame.setObjectName("BorderFrame")
    border_frame.setLayout(main_layout)
    border_frame.setFrameShape(QFrame.Shape.NoFrame)
    
    return border_frame
