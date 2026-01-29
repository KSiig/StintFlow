"""
Main application window.

Orchestrates the overall application layout with two panes:
- Left pane: Navigation menu (static)
- Right pane: Window buttons at top, switchable content area below

Manages window state and content switching.
"""

import sys

from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QStackedLayout,
    QWidget,
    QVBoxLayout,
    QFrame,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt, QEvent, QPoint, QRect
from PyQt6.QtGui import QMouseEvent

from .NavigationMenu import NavigationMenu
from .WindowButtons import WindowButtons
from .DraggableArea import DraggableArea
from .stint_tracking import OverviewMainWindow, ConfigMainWindow
from ui.models import ModelContainer, SelectionModel, NavigationModel
from ui.utilities import ResizeController


# Window configuration
WINDOW_X = 200
WINDOW_Y = 100
WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 832
WORKSPACE_MARGINS = 11
DRAGGABLE_AREA_HEIGHT = 40  # Height of the draggable area at the top
RESIZE_EDGE_MARGIN = 8  # Pixels from edge to trigger resize cursor/action


class MainWindow(QMainWindow):
    """
    Main application window with two-pane layout.
    
    Left pane: Static navigation menu
    Right pane: Window buttons (top) and switchable content area (below)
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize models
        self.selection_model = SelectionModel()
        self.navigation_model = NavigationModel()
        self.windows = {}
        
        # Initialize resize controller
        self.resize_controller = ResizeController(self, edge_margin=RESIZE_EDGE_MARGIN)
        
        self._setup_window_properties()
        self.navigation_menu = self._create_navigation_menu()
        self.window_buttons = self._create_window_buttons()
        self.central_scroll_area = self._create_scroll_area()
        self.central_container = self._create_central_container()
        self.draggable_area = self._create_draggable_area()
        
        # Create initial overview window and set as active
        models = ModelContainer(
            selection_model=self.selection_model,
            table_model=None  # TODO: Create TableModel when migrated
        )
        overview_window = OverviewMainWindow(models)
        self.navigation_model.add_widget(OverviewMainWindow, overview_window)
        self.navigation_model.set_active_widget(overview_window)
        
        # Create config window
        config_window = ConfigMainWindow(models)
        self.navigation_model.add_widget(ConfigMainWindow, config_window)
        
        self._assemble_main_window()
        
        # Enable mouse tracking on all widgets for resize cursor updates
        self._enable_mouse_tracking_recursive(self)
        
        # Install event filter to catch mouse moves over child widgets
        QApplication.instance().installEventFilter(self)

    def _setup_window_properties(self) -> None:
        """Configure basic window properties (size, flags, style)."""
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    def _create_window_buttons(self):
        """
        Create and return the window buttons component.
        
        Returns:
            WindowButtons: The configured window buttons instance
        """
        return WindowButtons(self)

    def _create_navigation_menu(self):
        """
        Create and return the navigation menu widget.
        
        Returns:
            NavigationMenu: The configured navigation menu instance
        """
        models = ModelContainer(
            selection_model=self.selection_model,
            navigation_model=self.navigation_model
        )
        return NavigationMenu(self, models=models)
    
    def _create_draggable_area(self):
        """
        Create draggable area for moving the frameless window.
        
        This widget is positioned absolutely at the top of the window
        and doesn't participate in any layout.
        
        Returns:
            DraggableArea: The draggable area widget
        """
        draggable = DraggableArea(self)
        # Position will be set in resizeEvent to keep it at the top
        return draggable

    def _create_scroll_area(self):
        """
        Create the scrollable content area.
        
        Returns:
            QScrollArea: The configured scroll area
        """
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        return scroll_area

    def _create_central_container(self):
        """
        Create the central container with stacked layout for view switching.
        
        Returns:
            QWidget: Container widget with stacked layout
        
        """

        # Connect navigation model signal to switch widgets
        self.navigation_model.activeWidgetChanged.connect(self._change_workspace_widget)

        container = QWidget()
        layout = QStackedLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.central_scroll_area.setWidget(container)
        self.central_container_layout = layout
        
        return container

    def _create_right_pane(self):
        """
        Create the right pane containing the content area.
        
        Note: Window buttons are positioned absolutely, not in this layout.
        
        Returns:
            QWidget: The right pane widget
        """
        pane = QWidget()
        layout = QVBoxLayout(pane)
        layout.setContentsMargins(WORKSPACE_MARGINS, 0, 0, WORKSPACE_MARGINS)
        layout.setSpacing(0)
        
        # Window buttons are positioned absolutely, not added to layout
        layout.addWidget(self.central_scroll_area)
        
        return pane

    def _assemble_main_window(self) -> None:
        """
        Assemble all layout components into the main window.
        
        Creates a border frame wrapper around the two-pane layout
        to provide consistent window borders.
        """
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, WORKSPACE_MARGINS, 0, 0)
        main_layout.setSpacing(0)
        
        # Left pane: Navigation menu (static)
        main_layout.addWidget(self.navigation_menu, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Right pane: Window buttons (top) and content area
        right_pane = self._create_right_pane()
        main_layout.addWidget(right_pane)
        
        # Border frame to wrap everything
        border_frame = QFrame()
        border_frame.setObjectName("BorderFrame")
        border_frame.setLayout(main_layout)
        border_frame.setFrameShape(QFrame.Shape.NoFrame)
        
        self.setCentralWidget(border_frame)
    
    def _enable_mouse_tracking_recursive(self, widget: QWidget) -> None:
        """
        Enable mouse tracking recursively for a widget and all its children.
        
        Args:
            widget: Widget to enable mouse tracking on
        """
        widget.setMouseTracking(True)
        for child in widget.findChildren(QWidget):
            child.setMouseTracking(True)

    def _change_workspace_widget(self) -> None:
        """
        Switch the active workspace widget.
        
        On first use, adds the widget to the stacked layout.
        Subsequent calls simply switch to the existing widget.
        """
        widget = self.navigation_model.active_widget
        
        if widget not in self.windows:
            # First time showing this widget, add it to layout
            widget.setParent(self.central_container)
            self.central_container_layout.addWidget(widget)
            self.windows[widget] = widget
        
        # Switch to the widget
        self.central_container_layout.setCurrentWidget(widget)
        # TODO: Implement additional model synchronization when table models are migrated
    
    def eventFilter(self, obj, event):
        """
        Event filter to catch mouse move events over child widgets.
        
        This ensures the resize cursor updates when hovering over edges,
        even when the mouse is over child widgets that would normally
        block mouseMoveEvent from reaching the main window.
        
        Args:
            obj: Object that received the event
            event: The event
            
        Returns:
            True if event was handled, False otherwise
        """
        # Only process events for widgets within this window
        if not isinstance(obj, QWidget) or (not self.isAncestorOf(obj) and obj != self):
            return super().eventFilter(obj, event)
        
        if event.type() == QEvent.Type.MouseMove and not self.resize_controller.is_resizing():
            # Convert mouse position to window coordinates
            global_pos = event.globalPosition().toPoint()
            window_pos = self.mapFromGlobal(global_pos)
            
            # Check if mouse is within window bounds
            if self.rect().contains(window_pos):
                # Update cursor based on edge proximity
                edge = self.resize_controller.get_resize_edge(window_pos)
                self.resize_controller.update_cursor(edge)
            else:
                # Mouse left the window, reset cursor
                self.unsetCursor()
        
        elif event.type() == QEvent.Type.Leave:
            # Mouse left the window, reset cursor if not resizing
            if not self.resize_controller.is_resizing():
                self.unsetCursor()
        
        return super().eventFilter(obj, event)
    
    def resizeEvent(self, event) -> None:
        """
        Handle window resize events.
        
        Updates the draggable area and window buttons positions.
        Both are positioned absolutely at the top of the window.        Ensures proper z-order with draggable area behind buttons.        """
        super().resizeEvent(event)
        
        # Position draggable area at the top, spanning the entire width
        self.draggable_area.setGeometry(0, 0, self.width(), DRAGGABLE_AREA_HEIGHT)
        
        # Position window buttons in the top-right corner
        # Get the actual width of the window buttons widget
        buttons_width = self.window_buttons.sizeHint().width()
        buttons_height = self.window_buttons.sizeHint().height()
        x_pos = self.width() - buttons_width - WORKSPACE_MARGINS
        y_pos = (DRAGGABLE_AREA_HEIGHT - buttons_height) // 2  # Center vertically in draggable area
        
        self.window_buttons.setGeometry(x_pos, y_pos, buttons_width, buttons_height)
        
        # Ensure proper z-order: draggable area behind, window buttons on top
        self.draggable_area.raise_()
        self.window_buttons.raise_()
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse move events for edge/corner resize cursor and resize action.
        
        Args:
            event: Mouse move event
        """
        if self.resize_controller.is_resizing():
            # Currently resizing - update window geometry
            self.resize_controller.update_resize(event.globalPosition().toPoint())
        else:
            # Not resizing - update cursor based on edge proximity
            edge = self.resize_controller.get_resize_edge(event.position().toPoint())
            self.resize_controller.update_cursor(edge)
        
        super().mouseMoveEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse press events to start edge resizing.
        
        Args:
            event: Mouse press event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            edge = self.resize_controller.get_resize_edge(event.position().toPoint())
            if edge:
                # Start resizing from this edge
                self.resize_controller.start_resize(edge, event.globalPosition().toPoint())
                event.accept()
                return
        
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse release events to stop edge resizing.
        
        Args:
            event: Mouse release event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            if self.resize_controller.is_resizing():
                # Stop resizing
                self.resize_controller.stop_resize()
                
                # Reset cursor based on current mouse position
                edge = self.resize_controller.get_resize_edge(event.position().toPoint())
                self.resize_controller.update_cursor(edge)
                
                event.accept()
                return
        
        super().mouseReleaseEvent(event)
    
    def changeEvent(self, event) -> None:
        """
        Handle window state changes.
        
        Updates the window buttons when window state changes (minimize, maximize, etc.).
        """
        if event.type() == QEvent.Type.WindowStateChange:
            self.window_buttons.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()

