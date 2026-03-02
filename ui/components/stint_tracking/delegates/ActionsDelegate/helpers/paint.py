"""Paint actions buttons for completed rows."""

from ui.models.TableRoles import TableRoles
from ui.models.table_constants import ColumnIndex


def paint(self, painter, option, index):
    status_idx = index.siblingAtColumn(ColumnIndex.STATUS)
    status = status_idx.data()
    if status is None or "Completed" not in str(status):
        super(type(self), self).paint(painter, option, index)
        return

    super(type(self), self).paint(painter, option, index)

    rects = self._button_rects(option.rect)
    row = index.row()
    model = index.model()
    meta = None
    if model is not None:
        meta = model.data(model.index(row, 0), TableRoles.MetaRole)
    excluded = bool(meta.get("excluded")) if isinstance(meta, dict) else False

    style = option.widget.style()
    for btn, rect in zip(self.buttons, rects):
        svg = btn.get("icon")
        text = btn.get("name", "")
        self._draw_button(painter, style, rect, svg_name=svg, text="" if svg else text, excluded=excluded)
