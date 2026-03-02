"""Dispatch mouse clicks to the correct action button."""


def _handle_mouse_click(self, event, model, option, index) -> bool:
    pos = event.position().toPoint()
    rects = self._button_rects(option.rect)

    for i, rect in enumerate(rects):
        if rect.contains(pos):
            name = self.buttons[i].get("name", "")
            row = index.row()
            if name == "exclude" and model is not None:
                self._toggle_exclude(row, model, option)
            self._emit_button_signals(name, row)
            return True
    return False
