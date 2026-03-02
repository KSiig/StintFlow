"""Handle editor events for action buttons."""

from ui.models.table_constants import ColumnIndex


def editor_event(self, event, model, option, index):
    status_idx = index.siblingAtColumn(ColumnIndex.STATUS)
    status = status_idx.data()
    if status is None or "Completed" not in str(status):
        return False

    if event.type() == event.Type.MouseButtonRelease:
        if hasattr(event, "position"):
            return self._handle_mouse_click(event, model, option, index)
    return False
