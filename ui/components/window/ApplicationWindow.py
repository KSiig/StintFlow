"""
Main application window.

Orchestrates the overall application layout with two panes:
- Left pane: Navigation menu (static)
- Right pane: Window buttons at top, switchable content area below

Manages window state, content switching, and event handling.
"""

from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QMouseEvent

from ..navigation import NavigationMenu
from .WindowButtons import WindowButtons
from ..common import DraggableArea
from ..stint_tracking import OverviewView, ConfigView
from ui.models import ModelContainer, SelectionModel, NavigationModel
from ui.utilities import ResizeController
from .layout_factory import (
    create_scroll_area,
    create_stacked_container,
    create_right_pane,
    create_main_layout
)
from .constants import (
    WINDOW_X,
    WINDOW_Y,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WORKSPACE_MARGINS,
    DRAGGABLE_AREA_HEIGHT,
    RESIZE_EDGE_MARGIN
)


class ApplicationWindow(QMainWindow):
    """
    Main application window with two-pane layout.
    
    Left pane: Static navigation menu
    Right pane: Window buttons (top) and switchable content area (below)
    """
    
    def __init__(self) -> None:
        super().__init__()
        
        # Initialize models
        self.selection_model = SelectionModel()
        self.navigation_model = NavigationModel()
        
        # Initialize resize controller
        self.resize_controller = ResizeController(self, edge_margin=RESIZE_EDGE_MARGIN)
        
        # Setup window and create components
        self._setup_window_properties()
        self._create_components()
        self._create_initial_views()
        self._assemble_layout()
        
        # Setup event handling
        self._setup_mouse_tracking()
        QApplication.instance().installEventFilter(self)

    def _setup_window_properties(self) -> None:
        """Configure basic window properties (size, flags, style)."""
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    
    def _create_components(self) -> None:
        """Create all window components."""
        # Models container
        models = ModelContainer(
            selection_model=self.selection_model,
            navigation_model=self.navigation_model
        )
        
        # Navigation and controls
        self.navigation_menu = NavigationMenu(self, models=models)
        self.window_buttons = WindowButtons(self)
        self.draggable_area = DraggableArea(self)
        
        # Content area with stacked layout
        self.central_scroll_area = create_scroll_area()
        self.central_container, self.central_container_layout = create_stacked_container(
            self.central_scroll_area
        )
        
        # Connect navigation model to view switching
        self.navigation_model.activeWidgetChanged.connect(self._change_workspace_widget)
    
    def _create_initial_views(self) -> None:
        """Create and register initial view windows."""
        models = ModelContainer(
            selection_model=self.selection_model,
            table_model=None  # TODO: Create TableModel when migrated
        )
        
        # Create overview view and set as active
        overview_view = OverviewView(models)
        self.navigation_model.add_widget(OverviewView, overview_view)
        self.navigation_model.set_active_widget(overview_view)
        
        # Create config view
        config_view = ConfigView(models)
        self.navigation_model.add_widget(ConfigView, config_view)
    
    def _assemble_layout(self) -> None:
        """Assemble all layout components into the main window."""
        right_pane = create_right_pane(self.central_scroll_area)
        border_frame = create_main_layout(self.navigation_menu, right_pane)
        self.setCentralWidget(border_frame)
    
    def _setup_mouse_tracking(self) -> None:
        """Enable mouse tracking for resize cursor updates."""
        self.setMouseTracking(True)
        # Enable on immediate children to catch edge hovers
        for child in self.findChildren(QWidget):
            if child.parent() == self:
                child.setMouseTracking(True)

    def _change_workspace_widget(self) -> None:
        """
        Switch the active workspace widget.
        
        Adds widget to stacked layout on first use, then switches to it.
        """
        widget = self.navigation_model.active_widget
        
        # Check if widget already in layout
        if self.central_container_layout.indexOf(widget) == -1:
            # First time showing this widget, add it to layout
            widget.setParent(self.central_container)
            self.central_container_layout.addWidget(widget)
        
        # Switch to the widget
        self.central_container_layout.setCurrentWidget(widget)
    
    def eventFilter(self, obj: QWidget, event: QEvent) -> bool:
        """
        Event filter to update resize cursor when hovering over edges.
        
        Catches mouse move events over child widgets to ensure cursor
        updates properly when near window edges.
        
        Args:
            obj: Object that received the event
            event: The event
            
        Returns:
            False to allow normal event processing
        """
        # Only process events for widgets within this window
        if not isinstance(obj, QWidget) or (not self.isAncestorOf(obj) and obj != self):
            return super().eventFilter(obj, event)
        
        if event.type() == QEvent.Type.MouseMove and not self.resize_controller.is_resizing():
            # Convert mouse position to window coordinates
            global_pos = event.globalPosition().toPoint()
            window_pos = self.mapFromGlobal(global_pos)
            
            # Update cursor if within window bounds
            if self.rect().contains(window_pos):
                edge = self.resize_controller.get_resize_edge(window_pos)
                self.resize_controller.update_cursor(edge)
        
        elif event.type() == QEvent.Type.Leave and not self.resize_controller.is_resizing():
            # Mouse left widget, reset cursor if not resizing
            self.unsetCursor()
        
        return super().eventFilter(obj, event)
    
    def resizeEvent(self, event: QEvent) -> None:
        """
        Handle window resize events.
        
        Updates positions of absolutely-positioned widgets (draggable area
        and window buttons) to keep them at the top of the window.
        
        Args:
            event: Resize event
        """
        super().resizeEvent(event)
        
        # Position draggable area at the top, spanning full width
        self.draggable_area.setGeometry(0, 0, self.width(), DRAGGABLE_AREA_HEIGHT)
        
        # Position window buttons in top-right corner
        buttons_width = self.window_buttons.sizeHint().width()
        buttons_height = self.window_buttons.sizeHint().height()
        x_pos = self.width() - buttons_width - WORKSPACE_MARGINS
        y_pos = (DRAGGABLE_AREA_HEIGHT - buttons_height) // 2  # Center vertically
        
        self.window_buttons.setGeometry(x_pos, y_pos, buttons_width, buttons_height)
        
        # Ensure proper z-order: draggable area behind, buttons on top
        self.draggable_area.raise_()
        self.window_buttons.raise_()
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse move events for resize cursor and resize action.
        
        Args:
            event: Mouse move event
        """
        if self.resize_controller.is_resizing():
            self.resize_controller.update_resize(event.globalPosition().toPoint())
        else:
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
        if event.button() == Qt.MouseButton.LeftButton and self.resize_controller.is_resizing():
            self.resize_controller.stop_resize()
            
            # Update cursor based on current position
            edge = self.resize_controller.get_resize_edge(event.position().toPoint())
            self.resize_controller.update_cursor(edge)
            
            event.accept()
            return
        
        super().mouseReleaseEvent(event)
    
    def changeEvent(self, event: QEvent) -> None:
        """
        Handle window state changes.
        
        Updates window buttons when window state changes (minimize, maximize, etc.).
        
        Args:
            event: State change event
        """
        if event.type() == QEvent.Type.WindowStateChange:
            self.window_buttons.window_state_changed(self.windowState())
        
        super().changeEvent(event)
        event.accept()

