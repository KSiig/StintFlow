"""Handle hover tooltips for action buttons."""

from PyQt6.QtWidgets import QToolTip

from ui.models.TableRoles import TableRoles


def help_event(self, event, view, option, index):
    try:
        pos = event.pos()
    except Exception:
        return super(type(self), self).helpEvent(event, view, option, index)

    rects = self._button_rects(option.rect)
    row = index.row()
    model = index.model()
    meta = None
    if model is not None:
        meta = model.data(model.index(row, 0), TableRoles.MetaRole)
    excluded = bool(meta.get("excluded")) if isinstance(meta, dict) else False

    for btn, rect in zip(self.buttons, rects):
        if rect.contains(pos):
            tip = btn.get("tooltip")
            name = btn.get("name", "")

            if isinstance(tip, dict):
                if name == "exclude":
                    if excluded:
                        text = tip.get("excluded") or tip.get("off") or tip.get("included")
                    else:
                        text = tip.get("included") or tip.get("on") or tip.get("excluded")
                else:
                    text = tip.get("text") or ""
            elif isinstance(tip, str):
                text = tip
            else:
                if name == "exclude":
                    text = "Include in mean" if excluded else "Exclude from mean"
                else:
                    text = name.capitalize()

            if text:
                QToolTip.showText(event.globalPos(), text, view)
                return True

    return super(type(self), self).helpEvent(event, view, option, index)
