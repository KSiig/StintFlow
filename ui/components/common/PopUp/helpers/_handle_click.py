"""Handle popup button clicks."""


def _handle_click(self, button_text: str) -> None:
    """Record which button was clicked and close the dialog."""
    self.clicked_button = button_text
    self.accept()
