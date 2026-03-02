"""Populate tire editor from model."""

from ui.models.TableRoles import TableRoles


def set_editor_data(self, editor, index):
    editor.blockSignals(True)
    self.tires_changed = index.data()
    self._update_button_text(editor.btn, index)
    editor.blockSignals(False)
