"""Update the status text on the loading overlay."""


def set_status(self, text: str) -> None:
    """Update the status label text."""
    self.status_label.setText(text)
