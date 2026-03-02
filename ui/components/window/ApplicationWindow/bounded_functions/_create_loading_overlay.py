from ui.components.common.LoadingOverlay import LoadingOverlay


def _create_loading_overlay(self) -> None:
    """Build the overlay widget displayed while initialization runs."""
    self.loading_overlay = LoadingOverlay(self.central_container)
    self.central_container_layout.addWidget(self.loading_overlay)
    self.central_container_layout.setCurrentWidget(self.loading_overlay)
