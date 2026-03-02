"""Show the dropdown popup above the button."""


def _show_popup(self) -> None:
    """Display the popup above the button with an 8px gap."""
    pos = self.btn.mapToGlobal(self.btn.rect().topLeft())
    self.popup.show()
    popup_height = self.popup.height()
    self.popup.move(pos.x(), pos.y() - popup_height - 8)
