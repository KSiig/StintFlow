from __future__ import annotations

from ...AgentCard import AgentCard


def set_agents(self, agents: list[dict]) -> None:
    """Populate the popup with cards for the connected agents."""
    cards_layout = getattr(self, "_cards_layout", None)
    content_widget = getattr(self, "_content_widget", None)
    scroll_area = getattr(self, "_scroll_area", None)
    if cards_layout is None:
        return
    while cards_layout.count():
        item = cards_layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
    for agent in agents:
        cards_layout.addWidget(AgentCard(agent))
    cards_layout.addStretch()

    if content_widget is not None and scroll_area is not None:
        cards_layout.invalidate()
        cards_layout.activate()
        content_widget.adjustSize()

        content_height = cards_layout.sizeHint().height()
        if content_height <= 0:
            content_height = content_widget.sizeHint().height()

        if agents:
            if content_height <= 0:
                content_height = max(getattr(self, "_last_scroll_height", 0), 1)
            target_height = min(content_height, 220)
            self._last_scroll_height = target_height
            scroll_area.setMinimumHeight(1)
            scroll_area.setMaximumHeight(220)
            scroll_area.setFixedHeight(target_height)
        else:
            self._last_scroll_height = 0
            scroll_area.setFixedHeight(0)

    self.adjustSize()
