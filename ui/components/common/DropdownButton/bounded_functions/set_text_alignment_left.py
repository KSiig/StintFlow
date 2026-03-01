"""Left-align text inside the dropdown button."""


def set_text_alignment_left(self, padding_left: int = 0) -> None:
    """Left-align the button text with optional padding."""
    if padding_left > 0:
        self.btn.setStyleSheet(f"text-align: left; padding-left: {padding_left}px;")
        return
    self.btn.setStyleSheet("text-align: left;")
