"""Show tooltip when badge is visible."""

from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QToolTip

from ui.models.TableRoles import TableRoles


def help_event(self, event, view, option, index):
    try:
        pos = event.pos()
    except Exception:
        return super(type(self), self).helpEvent(event, view, option, index)

    tire_data = index.data(TableRoles.TiresRole)
    badge_visible = False
    if isinstance(tire_data, dict):
        for wheel in ("fl", "fr", "rl", "rr"):
            comp_in = tire_data.get(wheel, {}).get("incoming", {}).get("compound") if isinstance(tire_data.get(wheel), dict) else None
            comp_out = tire_data.get(wheel, {}).get("outgoing", {}).get("compound") if isinstance(tire_data.get(wheel), dict) else None
            in_unknown = isinstance(comp_in, str) and comp_in.strip().lower() == "unknown"
            out_unknown = not isinstance(comp_out, str) or comp_out.strip().lower() == "unknown"
            if in_unknown and out_unknown:
                badge_visible = True
                break

    if not badge_visible:
        return super(type(self), self).helpEvent(event, view, option, index)

    tri_w = min(14, option.rect.width() // 6)
    pad = 4
    x0 = option.rect.left() + pad
    y0 = option.rect.top() + pad
    badge_rect = QRect(x0, y0, tri_w, tri_w)

    if badge_rect.contains(pos):
        QToolTip.showText(event.globalPos(), "Tires need to be set manually", view)
        return True

    return super(type(self), self).helpEvent(event, view, option, index)
