from PyQt6.QtCore import QObject, pyqtSignal

class NavigationModel(QObject):
    activeWidgetChanged = pyqtSignal(object)
    selectionChanged = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._active_widget = None

    @property
    def active_widget(self):
        return self._active_widget

    def set_active_widget(self, active_widget):
        if active_widget!= self._active_widget:
            self._active_widget = active_widget
            self.activeWidgetChanged.emit(active_widget)
            self.selectionChanged.emit(self._active_widget)
