"""Paint model background and attention badge."""

from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QColor, QPolygon

from ui.components.stint_tracking.delegates.delegate_utils import paint_model_background
from ui.models.TableRoles import TableRoles


def paint(self, painter, option, index):
    paint_model_background(painter, option, index)
    super(type(self), self).paint(painter, option, index)

    tire_data = index.data(TableRoles.TiresRole)
    unknown_found = False
    tri_w = min(14, option.rect.width() // 6)
    if isinstance(tire_data, dict):
        for pos in ("fl", "fr", "rl", "rr"):
            comp_in = tire_data.get(pos, {}).get("incoming", {}).get("compound") if isinstance(tire_data.get(pos), dict) else None
            comp_out = tire_data.get(pos, {}).get("outgoing", {}).get("compound") if isinstance(tire_data.get(pos), dict) else None
            in_unknown = isinstance(comp_in, str) and comp_in.strip().lower() == "unknown"
            out_unknown = not isinstance(comp_out, str) or comp_out.strip().lower() == "unknown"
            if in_unknown and out_unknown:
                unknown_found = True
                break

    if unknown_found:
        painter.save()
        badge_size = tri_w
        pad = 4
        x0 = option.rect.left() + pad
        y0 = option.rect.top() + pad
        p1 = QPoint(x0, y0)
        p2 = QPoint(x0 + badge_size, y0)
        p3 = QPoint(x0, y0 + badge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#FF3B30"))
        painter.drawPolygon(QPolygon([p1, p2, p3]))
        painter.restore()
    else:
        painter.setPen(option.palette.color(option.palette.ColorRole.Text))
        text_rect = option.rect.adjusted(tri_w + 8, 0, 0, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, "")
