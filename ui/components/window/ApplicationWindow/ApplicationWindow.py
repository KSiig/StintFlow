from __future__ import annotations

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.models import NavigationModel, SelectionModel
from ui.utilities import ResizeController
from ui.utilities.loading_queue import LoadingQueue

from .bounded_functions._assemble_layout import _assemble_layout
from .bounded_functions._change_event import changeEvent
from .bounded_functions._change_workspace_widget import _change_workspace_widget
from .bounded_functions._create_components import _create_components
from .bounded_functions._create_loading_overlay import _create_loading_overlay
from .bounded_functions._hide_loading import hide_loading
from .bounded_functions._mouse_move_event import mouseMoveEvent
from .bounded_functions._mouse_press_event import mousePressEvent
from .bounded_functions._mouse_release_event import mouseReleaseEvent
from .bounded_functions._on_connection_failed import _on_connection_failed
from .bounded_functions._on_initialization_done import _on_initialization_done
from .bounded_functions._resize_event import resizeEvent
from .bounded_functions._setup_mouse_tracking import _setup_mouse_tracking
from .bounded_functions._setup_window_properties import _setup_window_properties
from .bounded_functions._show_loading import show_loading
from .bounded_functions._start_initialization import _start_initialization
from .bounded_functions.closeEvent import closeEvent
from .bounded_functions.event_filter import eventFilter
from .bounded_functions.show_settings import show_settings


class ApplicationWindow(QMainWindow):
    """Main application window with navigation and content panes."""

    _setup_window_properties = _setup_window_properties
    _create_components = _create_components
    _create_loading_overlay = _create_loading_overlay
    _start_initialization = _start_initialization
    show_loading = show_loading
    hide_loading = hide_loading
    _on_connection_failed = _on_connection_failed
    _on_initialization_done = _on_initialization_done
    _assemble_layout = _assemble_layout
    _setup_mouse_tracking = _setup_mouse_tracking
    _change_workspace_widget = _change_workspace_widget
    eventFilter = eventFilter
    resizeEvent = resizeEvent
    mouseMoveEvent = mouseMoveEvent
    mousePressEvent = mousePressEvent
    mouseReleaseEvent = mouseReleaseEvent
    changeEvent = changeEvent
    closeEvent = closeEvent
    show_settings = show_settings

    def __init__(self) -> None:
        super().__init__()

        self.selection_model = SelectionModel()
        self.navigation_model = NavigationModel()
        self.resize_controller = ResizeController(self)

        self._setup_window_properties()
        self._create_components()
        self._assemble_layout()
        self._create_loading_overlay()

        self._loading_widget_stack: list = []
        LoadingQueue.register_window(self)
        QTimer.singleShot(0, self._start_initialization)

        self._setup_mouse_tracking()
        QApplication.instance().installEventFilter(self)
