from __future__ import annotations


def _toggle_edit(self) -> None:
    """Toggle edit mode for inputs and buttons."""
    edit_mode = self.save_btn.isVisible()
    if edit_mode:
        self.save_btn.hide()
        self.edit_btn.show()
    else:
        self.edit_btn.hide()
        self.save_btn.show()

    for widget in self.inputs.values():
        try:
            if hasattr(widget, 'setReadOnly'):
                widget.setReadOnly(edit_mode)
                widget.setProperty('editable', not edit_mode)
                widget.style().unpolish(widget)
                widget.style().polish(widget)
                continue
        except Exception:
            pass

        try:
            widget.setEnabled(not edit_mode)
        except Exception:
            pass
