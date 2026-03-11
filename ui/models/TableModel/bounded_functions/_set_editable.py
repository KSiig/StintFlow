"""Enable or disable editing mode on the model."""


def set_editable(self, *, editable: bool, partial: bool = False) -> None:
    """Configure edit mode.

    Parameters:
    editable (bool): Toggles whether the table accepts edits.
    partial (bool, optional): Controls whether edits apply to a subset of cells/rows.
        - partial=True: Enable editing only for cells/rows marked editable or a currently selected region.
        - partial=False: Enable full-table editing.

    Side-effects:
    - When partial=True, editing is restricted to cells/rows explicitly marked editable or the current selection.
    - Callers switching modes should ensure that per-cell permissions or selection states are consistent with the desired behavior.
    """
    self.editable = editable
    self.partial = partial
