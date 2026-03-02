def hide_loading(self) -> None:
    """Hide the loading overlay and restore the previous view."""
    if not hasattr(self, "loading_overlay") or not self.loading_overlay:
        return

    target = None
    if self._loading_widget_stack:
        target = self._loading_widget_stack.pop()

    if hasattr(self, "central_container_layout"):
        if target is not None:
            try:
                self.central_container_layout.setCurrentWidget(target)
                return
            except Exception:
                pass

        if hasattr(self, "navigation_model"):
            active = self.navigation_model.active_widget
            if active is not None:
                self.central_container_layout.setCurrentWidget(active)
                return

        self.loading_overlay.hide()
    else:
        self.loading_overlay.hide()
