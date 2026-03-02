from core.errors.log_error import log_exception


def _change_workspace_widget(self) -> None:
    """Switch the active workspace widget and manage stacked layout."""
    widget = self.navigation_model.active_widget

    for i in reversed(range(self.central_container_layout.count())):
        candidate = self.central_container_layout.widget(i)
        if candidate is widget or candidate is getattr(self, "loading_overlay", None):
            continue
        self.central_container_layout.removeWidget(candidate)
        candidate.setParent(None)

    if self.central_container_layout.indexOf(widget) == -1:
        widget.setParent(self.central_container)
        self.central_container_layout.addWidget(widget)

    self.central_container_layout.setCurrentWidget(widget)

    try:
        widget.adjustSize()
        self.central_container.adjustSize()
        if hasattr(self, "central_scroll_area") and self.central_scroll_area.widget():
            self.central_scroll_area.widget().updateGeometry()
        if hasattr(self, "central_scroll_area"):
            vs = self.central_scroll_area.verticalScrollBar()
            if vs:
                vs.setValue(0)
    except Exception as exc:  # pragma: no cover - defensive logging
        log_exception(exc, "Error adjusting geometry after workspace switch", category="ui", action="switch_workspace")
