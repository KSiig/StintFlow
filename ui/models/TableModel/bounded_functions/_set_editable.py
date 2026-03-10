"""Enable or disable editing mode on the model."""


def set_editable(self, editable: bool, partial: bool = False) -> None:
    """Configure edit mode."""
    self.editable = editable
    self.partial = partial
