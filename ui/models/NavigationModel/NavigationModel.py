from PyQt6.QtCore import QObject, pyqtSignal

from .bounded_functions._add_widget import _add_widget
from .bounded_functions._set_active_widget import _set_active_widget


class NavigationModel(QObject):
    """Model for managing navigation state and active widgets."""

    activeWidgetChanged = pyqtSignal(object)
    widgetAdded = pyqtSignal(object)
    selectionChanged = pyqtSignal(object)

    _set_active_widget = _set_active_widget
    _add_widget = _add_widget

    def __init__(self):
        super().__init__()
        self._active_widget = None
        self._widgets = {}

    @property
    def active_widget(self):
        return self._active_widget

    @property
    def widgets(self):
        return self._widgets

    def set_active_widget(self, active_widget):
        self._set_active_widget(active_widget)

    def add_widget(self, widget_cls, widget):
        self._add_widget(widget_cls, widget)
