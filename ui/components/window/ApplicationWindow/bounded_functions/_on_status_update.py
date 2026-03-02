def _on_status_update(self, message: str) -> None:
    """Update overlay text while the worker runs."""
    if hasattr(self, "loading_overlay") and self.loading_overlay:
        self.loading_overlay.set_status(message)
