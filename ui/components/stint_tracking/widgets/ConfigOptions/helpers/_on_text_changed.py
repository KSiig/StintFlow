"""Show save button when text changes."""

def _on_text_changed(self) -> None:
    """Handle text changes in input fields."""
    if self._is_restoring_form_state:
        return

    self._has_unsaved_form_changes = True
    self.save_btn.show()
    self.cancel_btn.show()