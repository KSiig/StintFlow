from PyQt6.QtCore import QObject, pyqtSignal

class NavigationModel(QObject):
    activeWidgetChanged = pyqtSignal(object)
    widgetAdded = pyqtSignal(object)
    selectionChanged = pyqtSignal(object)

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
        if active_widget!= self._active_widget:
            self._active_widget = active_widget
            self.activeWidgetChanged.emit(active_widget)
            self.selectionChanged.emit(self._active_widget)

    def add_widget(self, widget_cls, widget):
        self._widgets[widget_cls] = widget
        self.widgetAdded.emit(widget)
