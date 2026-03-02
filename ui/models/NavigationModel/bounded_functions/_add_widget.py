def _add_widget(self, widget_cls, widget):
    """Register a widget instance for a widget class."""
    self._widgets[widget_cls] = widget
    self.widgetAdded.emit(widget)
