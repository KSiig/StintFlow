from PyQt6.QtWidgets import QHBoxLayout

from core.utilities import resource_path


def _create_layout(self) -> None:
    """Create and configure the window buttons layout."""
    layout = QHBoxLayout(self)
    layout.setContentsMargins(0, self.BUTTON_CONTAINER_MARGIN_TOP, self.BUTTON_CONTAINER_MARGIN_RIGHT, 0)
    layout.setSpacing(self.BUTTON_SPACING)

    self.min_button = self._create_button(
        resource_path(self.BUTTON_ICONS["minimize"]),
        self.window().showMinimized,
    )

    self.max_button = self._create_button(
        resource_path(self.BUTTON_ICONS["maximize"]),
        self.window().showMaximized,
    )

    self.close_button = self._create_button(
        resource_path(self.BUTTON_ICONS["close"]),
        self.window().close,
    )

    self.restart_button = self._create_button(
        resource_path(self.BUTTON_ICONS["restart"]),
        self._restart_app,
    )
    self.restart_button.setToolTip("Restart")
    self.restart_button.setVisible(self._should_show_restart())

    self.normal_button = self._create_button(
        resource_path(self.BUTTON_ICONS["restore"]),
        self.window().showNormal,
    )
    self.normal_button.setVisible(False)

    for button in [
        self.min_button,
        self.normal_button,
        self.max_button,
        self.restart_button,
        self.close_button,
    ]:
        layout.addWidget(button)

    layout.addStretch()
