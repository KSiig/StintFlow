def _set_active_widget(self, active_widget):
    """Set the currently active widget and emit signals when it changes."""
    if active_widget != self._active_widget:
        self._active_widget = active_widget
        self.activeWidgetChanged.emit(active_widget)
        self.selectionChanged.emit(self._active_widget)
