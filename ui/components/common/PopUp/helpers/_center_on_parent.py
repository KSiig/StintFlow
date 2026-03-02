"""Center the popup dialog on its parent or screen."""


def _center_on_parent(self) -> None:
    """Center the dialog on the parent window or screen."""
    self.adjustSize()
    parent = self.parent()
    if parent:
        window = parent.window()
        center_point = window.frameGeometry().center()
    else:
        center_point = self.screen().availableGeometry().center()

    rect = self.frameGeometry()
    rect.moveCenter(center_point)
    self.move(rect.topLeft())
