"""Populate stint type editor from the model."""


def set_editor_data(self, editor, index):
    editor.dropdown.set_value(str(index.data()))
