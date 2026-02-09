"""
Navigation model for managing active workspace widget.

Tracks which widget is currently displayed in the main content area.
"""

from PyQt6.QtCore import QObject, pyqtSignal


class NavigationModel(QObject):
    """
    Model for managing navigation state and active widgets.
    
    Signals:
        activeWidgetChanged: Emitted when the active widget changes
        widgetAdded: Emitted when a new widget is registered
        selectionChanged: Emitted when active widget selection changes
    """
    
    activeWidgetChanged = pyqtSignal(object)
    widgetAdded = pyqtSignal(object)
    selectionChanged = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._active_widget = None
        self._widgets = {}

    @property
    def active_widget(self):
        """Get the currently active widget class."""
        return self._active_widget

    @property
    def widgets(self):
        """Get the dictionary of registered widgets."""
        return self._widgets

    def set_active_widget(self, active_widget):
        """
        Set the currently active widget.
        
        Args:
            active_widget: Widget class to set as active
        """
        if active_widget != self._active_widget:
            self._active_widget = active_widget
            self.activeWidgetChanged.emit(active_widget)
            self.selectionChanged.emit(self._active_widget)

    def add_widget(self, widget_cls, widget):
        """
        Register a widget instance for a widget class.
        
        Args:
            widget_cls: Widget class (used as key)
            widget: Widget instance to register
        """
        self._widgets[widget_cls] = widget
        self.widgetAdded.emit(widget)
