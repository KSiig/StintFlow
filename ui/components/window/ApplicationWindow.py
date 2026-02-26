"""
Main application window.

Orchestrates the overall application layout with two panes:
- Left pane: Navigation menu (static)
- Right pane: Window buttons at top, switchable content area below

Manages window state, content switching, and event handling.
"""

from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt6.QtCore import Qt, QEvent, QTimer
from PyQt6.QtGui import QMouseEvent

from core.errors.log_error import log_exception

from ..navigation import NavigationMenu
from .WindowButtons import WindowButtons
from ..common import DraggableArea
from ..common.LoadingOverlay import LoadingOverlay
from ..stint_tracking import OverviewView, ConfigView, StrategiesView
from ..settings import SettingsView
from ui.models import ModelContainer, SelectionModel, NavigationModel
from ui.utilities import ResizeController
from ui.utilities.initialization_worker import InitializationWorker
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
    WORKSPACE_MARGINS_HOR,
    DRAGGABLE_AREA_HEIGHT,
    RESIZE_EDGE_MARGIN
)
from ..stint_tracking import get_header_titles
from ui.models import TableModel


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
        self._assemble_layout()
        
        # prepare loading overlay and defer heavy initialization
        self._create_loading_overlay()
        # initialize stack used by show_loading/hide_loading helpers
        self._loading_widget_stack = []
        QTimer.singleShot(0, self._start_initialization)

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
    
    def _create_loading_overlay(self) -> None:
        """Build the overlay widget that is displayed while initialization runs."""
        # We add the overlay as another widget in the stacked container so it
        # can be shown by simply switching the current widget; it will cover the
        # same area as the future views.
        self.loading_overlay = LoadingOverlay(self.central_container)
        self.central_container_layout.addWidget(self.loading_overlay)
        self.central_container_layout.setCurrentWidget(self.loading_overlay)

    def _start_initialization(self) -> None:
        """Begin the asynchronous view/data setup.

        The background worker handles database connectivity testing and will
        emit a failure signal if it cannot connect.  We simply prepare an empty
        model and start the worker here.
        """
        # create an empty model first (no DB load)
        self.table_model = TableModel(
            selection_model=self.selection_model,
            headers=get_header_titles(),
            load_on_init=False
        )

        # ensure the overlay has a starting message
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.set_status('Initializing...')

        # run a worker thread to fetch the data
        self._init_worker = InitializationWorker(self.selection_model)
        self._init_worker.status.connect(self._on_status_update)
        self._init_worker.connectionFailed.connect(self._on_connection_failed)
        self._init_worker.finished.connect(self._on_initialization_done)
        self._init_worker.start()

    def _on_status_update(self, message: str) -> None:
        """Update overlay text while the worker runs."""
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.set_status(message)

    # centralized helpers ---------------------------------------------------
    def show_loading(self, message: str) -> None:
        """Display the global loading overlay with *message*.

        The current visible widget is pushed onto an internal stack; when
        ``hide_loading`` is called the last widget is popped and restored.  This
        allows overlapping calls (e.g. Strategy view and table update) without
        losing track of the proper return state.
        """
        if not hasattr(self, 'loading_overlay') or not self.loading_overlay:
            return

        self.loading_overlay.set_status(message)
        from PyQt6.QtWidgets import QApplication

        if hasattr(self, 'central_container_layout'):
            try:
                current = self.central_container_layout.currentWidget()
            except Exception:
                current = None
            self._loading_widget_stack.append(current)
            self.central_container_layout.setCurrentWidget(self.loading_overlay)
        else:
            # no stacked layout; just make it visible and push None to keep
            # stack balanced
            self._loading_widget_stack.append(None)
            self.loading_overlay.show()

        # force immediate paint of overlay so it appears before any blocking work
        QApplication.processEvents()

    def hide_loading(self) -> None:
        """Hide the loading overlay and restore the previous view.

        Pops the last widget off the stack and makes it current.  If the stack is
        empty the overlay is simply hidden (or the navigation model's active
        widget is used as a fallback).
        """
        if not hasattr(self, 'loading_overlay') or not self.loading_overlay:
            return

        target = None
        if self._loading_widget_stack:
            target = self._loading_widget_stack.pop()

        if hasattr(self, 'central_container_layout'):
            if target is not None:
                try:
                    self.central_container_layout.setCurrentWidget(target)
                    return
                except Exception:
                    pass
            # nothing explicit to restore; try navigation model
            if hasattr(self, 'navigation_model'):
                active = self.navigation_model.active_widget
                if active is not None:
                    self.central_container_layout.setCurrentWidget(active)
                    return
            # still here? just hide overlay
            self.loading_overlay.hide()
        else:
            self.loading_overlay.hide()

    # end helpers ---------------------------------------------------------

    def _on_connection_failed(self) -> None:
        """Worker reported database connection failure.

        Switch to settings pane and hide the overlay so the user can correct
        the credentials.  This runs on the main thread.
        """
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.set_status('Connection failed')

        # show settings view
        models = ModelContainer(selection_model=self.selection_model)
        settings_view = SettingsView(models)
        self.navigation_model.add_widget(SettingsView, settings_view)
        self.navigation_model.set_active_widget(settings_view)
        settings_view.alert_db_connection_failure()

        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.hide()

    def _on_initialization_done(self, data, tires, mean_stint_time, events, sessions) -> None:
        """Called once the worker has finished loading data.

        This method creates the actual application views using the now-populated
        table model, updates the session picker with pre-fetched navigation data,
        switches away from the loading overlay, and sets the default active page.
        """
        # populate model with results
        self.table_model.update_data(data=data, tires=tires, mean_stint_time=mean_stint_time)

        # update session picker without further DB access
        try:
            if hasattr(self, 'navigation_menu') and hasattr(self.navigation_menu, 'session_picker'):
                sp = self.navigation_menu.session_picker
                sp.events.blockSignals(True)
                sp.sessions.blockSignals(True)
                sp.events.clear()
                for doc in events:
                    sp.events.addItem(doc.get('name',''), userData=str(doc.get('_id','')))
                if events and sessions:
                    sp.sessions.clear()
                    for doc in sessions:
                        sp.sessions.addItem(doc.get('name',''), userData=str(doc.get('_id','')))
                sp.events.blockSignals(False)
                sp.sessions.blockSignals(False)
                sp.reload(selected_event_id=self.selection_model.event_id, selected_session_id=self.selection_model.session_id)
        except Exception:
            pass  # failure here shouldn't crash startup

        models = ModelContainer(
            selection_model=self.selection_model,
            table_model=self.table_model
        )

        # create and register views just as before
        overview_view = OverviewView(models)
        self.navigation_model.add_widget(OverviewView, overview_view)

        config_view = ConfigView(models)
        self.navigation_model.add_widget(ConfigView, config_view)

        strategies_view = StrategiesView(models)
        self.navigation_model.add_widget(StrategiesView, strategies_view)

        settings_view = SettingsView(models)
        self.navigation_model.add_widget(SettingsView, settings_view)

        # switch to the overview once ready
        self.navigation_model.set_active_widget(overview_view)

        # hide overlay
        if hasattr(self, 'loading_overlay') and self.loading_overlay:
            self.loading_overlay.hide()
    
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
        
        Only the current page (plus the loading overlay) is kept in the stacked
        layout at any given time.  This avoids the default behaviour of
        ``QStackedLayout`` which calculates its size hint as the maximum size
        hint of *all* children; when a very tall widget (e.g. ``ConfigView``)
        is added the layout would remain that height even after switching to a
        shorter page, causing strange overflow when the scroll area was used.

        By removing previous widgets from the layout we ensure the container's
        size hint is based solely on the active widget.  The removed widgets
        are not deleted; they are simply reparented later when they become
        active again, so their state is preserved.

        After switching we also force a geometry recalculation and reset the
        scroll position so that the scroll area behaves correctly.
        """
        widget = self.navigation_model.active_widget

        # remove any non-current, non-overlay widgets from the layout; keep
        # the widget objects alive so they can be re-added later
        for i in reversed(range(self.central_container_layout.count())):
            w = self.central_container_layout.widget(i)
            if w is widget or w is getattr(self, 'loading_overlay', None):
                continue
            self.central_container_layout.removeWidget(w)
            w.setParent(None)

        # Add the widget if it's not already present
        if self.central_container_layout.indexOf(widget) == -1:
            widget.setParent(self.central_container)
            self.central_container_layout.addWidget(widget)

        # Switch to the widget
        self.central_container_layout.setCurrentWidget(widget)

        # Force geometry recalculation so that the scroll area shrinks to the
        # natural size of the new widget rather than staying at the previous
        # (potentially larger) height.  See issue described in bug report:
        # switching from tall ConfigView to shorter StrategiesView left the
        # stacked container at the old height which made strategy settings
        # panels stretch past the bottom of the window.
        try:
            widget.adjustSize()
            self.central_container.adjustSize()
            # updateGeometry on the scroll area's inner widget also helps
            if hasattr(self, 'central_scroll_area') and self.central_scroll_area.widget():
                self.central_scroll_area.widget().updateGeometry()
            # reset vertical scroll so new page is shown from top
            if hasattr(self, 'central_scroll_area'):
                vs = self.central_scroll_area.verticalScrollBar()
                if vs:
                    vs.setValue(0)
        except Exception as e:
            # non‑critical; just log and continue silently
            log_exception(e, 'Error adjusting geometry after workspace switch',
                         category='ui', action='switch_workspace')

            pass
    
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
        x_pos = self.width() - buttons_width - WORKSPACE_MARGINS_HOR
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
    
    def show_settings(self) -> None:
        """
        Switch the main window to the settings view.

        This is useful when the application starts and detects a problem with
        database connectivity; we can send the user directly to the settings
        panel so they can correct their configuration.
        """
        settings_widget = self.navigation_model.widgets.get(SettingsView)
        if settings_widget:
            self.navigation_model.set_active_widget(settings_widget)

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

