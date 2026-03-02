from PyQt6.QtWidgets import QApplication


def show_loading(self, message: str) -> None:
    """Display the global loading overlay with message."""
    if not hasattr(self, "loading_overlay") or not self.loading_overlay:
        return

    self.loading_overlay.set_status(message)

    if hasattr(self, "central_container_layout"):
        current = None
        try:
            current = self.central_container_layout.currentWidget()
        except Exception:
            current = None
        self._loading_widget_stack.append(current)
        self.central_container_layout.setCurrentWidget(self.loading_overlay)
    else:
        self._loading_widget_stack.append(None)
        self.loading_overlay.show()

    QApplication.processEvents()
