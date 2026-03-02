from PyQt6.QtCore import Qt


def window_state_changed(self, state: Qt.WindowState) -> None:
    """Update button visibility based on window state."""
    is_maximized = bool(state & Qt.WindowState.WindowMaximized)
    self.normal_button.setVisible(is_maximized)
    self.max_button.setVisible(not is_maximized)
